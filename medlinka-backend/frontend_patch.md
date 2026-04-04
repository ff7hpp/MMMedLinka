# MedLinka Frontend Connection Patch Guide

Here is exactly how to update `MedLinka.html` to connect to the real FastAPI backend.
Replace all the mock functions in `MedLinka.html` with the new `fetch()` API calls below.

> **Global Setup**: Add a `let currentToken = null;` at the top of your state, and define `BASE_URL = "http://localhost:8000/api";` 

### 1. doRegister()
❌ ORIGINAL MOCK CODE:
```javascript
function doRegister() {
  const name = document.getElementById('regName').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const pass = document.getElementById('regPass').value;
  const pass2 = document.getElementById('regPass2').value;
  if (!name || !email || !pass) return showToast(t('errFill'), 'warn');
  if (pass !== pass2) return showToast(t('errPass'), 'warn');
  currentUser = { name, email };
  enterApp();
}
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function doRegister() {
  const name = document.getElementById('regName').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const pass = document.getElementById('regPass').value;
  const pass2 = document.getElementById('regPass2').value;
  if (!name || !email || !pass) return showToast(t('errFill'), 'warn');
  if (pass !== pass2) return showToast(t('errPass'), 'warn');
  
  try {
      const res = await fetch(`${BASE_URL}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: name, email: email, password: pass })
      });
      if (!res.ok) throw new Error("Registration failed");
      const data = await res.json();
      currentToken = data.token;
      currentUser = data.user;
      enterApp();
  } catch (err) {
      showToast(err.message, 'warn');
  }
}
```

### 2. doLogin()
❌ ORIGINAL MOCK CODE:
```javascript
function doLogin() {
  const email = document.getElementById('loginEmail').value.trim();
  const pass = document.getElementById('loginPass').value;
  if (!email || !pass) return showToast(t('errFill'), 'warn');
  currentUser = { name: email.split('@')[0], email };
  enterApp();
}
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function doLogin() {
  const email = document.getElementById('loginEmail').value.trim();
  const pass = document.getElementById('loginPass').value;
  if (!email || !pass) return showToast(t('errFill'), 'warn');
  
  try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, password: pass })
      });
      if (!res.ok) throw new Error("Invalid email or password");
      const data = await res.json();
      currentToken = data.token;
      currentUser = data.user;
      enterApp();
  } catch (err) {
      showToast(err.message, 'warn');
  }
}
```

### 3. getAIResp() / sendMsg()
❌ ORIGINAL MOCK CODE:
```javascript
function sendMsg() {
  // ...
  setTimeout(() => {
    removeTyping(typId);
    addBotMsg(getAIResp(msg));
  }, 1000 + Math.random() * 800);
}
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function sendMsg() {
  const inp = document.getElementById('chatInput');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';
  addUserMsg(msg);
  document.getElementById('chipsRow').style.display = 'none';
  
  const typId = showTyping();
  
  try {
      const res = await fetch(`${BASE_URL}/chat/send`, {
          method: "POST",
          headers: { 
              "Content-Type": "application/json",
              "Authorization": `Bearer ${currentToken}`
          },
          body: JSON.stringify({ message: msg })
      });
      if (!res.ok) throw new Error("AI error");
      const data = await res.json();
      removeTyping(typId);
      addBotMsg(data.reply);
  } catch(err) {
      removeTyping(typId);
      addBotMsg("Sorry, the AI is unavailable right now.");
  }
}
```

### 4. renderDoctorsList() / fetch real doctors
❌ ORIGINAL MOCK CODE:
```javascript
// Relies on static `doctorsData` array
function renderDoctorsList(list) { ... }
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function fetchDoctors(specialty = "all") {
    try {
        const query = specialty && specialty !== 'all' && specialty !== 'All' ? `?specialty=${specialty}` : '';
        const res = await fetch(`${BASE_URL}/doctors${query}`, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        const docs = await res.json();
        // Since original UI assumes certain properties, map the returned doctor list
        const uiDocs = docs.map(d => ({
            id: d.id, name: d.name, spec_en: d.specialty, spec_ar: d.specialty, spec_tr: d.specialty,
            rating: d.rating, patients: '100+', exp: '10y', emoji: '👨‍⚕️', color: '#d4f5e9', filter: d.specialty
        }));
        renderDoctorsList(uiDocs);
    } catch(e) {
        console.error(e);
    }
}
// Call fetchDoctors('all') instead of renderDoctorsList(doctorsData)
```

### 5. renderMedGrid() / fetch mediciness
❌ ORIGINAL MOCK CODE:
```javascript
function renderMedGrid(list) { ... }
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function searchPharmacy(query) {
    if (!query) query = "panadol"; // default
    try {
        const res = await fetch(`${BASE_URL}/medicines/search?q=${query}`, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        const meds = await res.json();
        const uiMeds = meds.map((m, i) => ({
            id: i + 1, emoji: '💊', name_en: m.brand_name || m.generic_name || 'Medicine',
            name_ar: m.brand_name || 'Medicine', name_tr: m.brand_name || 'Medicine',
            desc_en: (m.purpose || '').substring(0, 50),
            price: `$${(Math.random()*10 + 5).toFixed(2)}` // API doesn't have prices
        }));
        renderMedGrid(uiMeds);
    } catch(e) {
        console.error(e);
    }
}
```

### 6. renderReminderList()
❌ ORIGINAL MOCK CODE:
```javascript
function renderReminderList() { ... using static remindersData }
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function fetchReminders() {
    try {
        const res = await fetch(`${BASE_URL}/reminders`, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        const data = await res.json();
        const container = document.getElementById('reminderList');
        container.innerHTML = data.map(r => `
            <div class="rem-card">
              <div class="rem-icon" style="background:#e3f2fd">💊</div>
              <div class="rem-info">
                <div class="rem-name">${r.medicine}</div>
                <div class="rem-detail">${r.dose} - ${r.frequency}</div>
                <div class="rem-times"><span class="rem-time-chip">${r.time}</span></div>
              </div>
            </div>
        `).join('');
    } catch(e) {
        console.error(e);
    }
}
```

### 7. Place Order
❌ ORIGINAL MOCK CODE:
```javascript
function checkout() {
  cart = []; updateCartBar(); closeCartSheet();
  showToast(t('toastOrder'), 'success');
}
```

✅ REAL API CALL REPLACEMENT:
```javascript
async function checkout() {
    if(cart.length === 0) return;
    try {
        const items = cart.map(c => ({ name: c.name_en, qty: c.qty, price: parseFloat(c.price.replace('$','')) }));
        const res = await fetch(`${BASE_URL}/orders/place`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${currentToken}`
            },
            body: JSON.stringify({ items })
        });
        if(res.ok) {
            cart = []; updateCartBar(); closeCartSheet();
            showToast(t('toastOrder'), 'success');
        }
    } catch(e) {
        console.error(e);
        showToast("Error placing order", "warn");
    }
}
```
