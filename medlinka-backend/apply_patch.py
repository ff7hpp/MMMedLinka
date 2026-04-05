import re

def apply_patch():
    file_path = "../MedLinka.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Add BASE_URL and currentToken if not there
        if "let currentToken = null;" not in html:
            html = html.replace("let currentUser = null;", "let currentUser = null;\nlet currentToken = null;\nconst BASE_URL = 'http://127.0.0.1:8000/api';")

        print("Original HTML length:", len(html))

        # 1. doRegister
        html = re.sub(r'function doRegister\(\)\s*\{[^{]*?enterApp\(\);\s*\}', 
"""async function doRegister() {
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
}""", html)

        # 2. doLogin
        html = re.sub(r'function doLogin\(\)\s*\{[^{]*?enterApp\(\);\s*\}', 
"""async function doLogin() {
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
      currentToken = data.access_token || data.token; // Handle standard token formats
      currentUser = data.user;
      enterApp();
  } catch (err) {
      showToast(err.message, 'warn');
  }
}""", html)

        # 3. sendMsg
        html = re.sub(r'function sendMsg\(\)\s*\{(?:[^{}]*|\{[^{}]*\})*\}', 
"""async function sendMsg() {
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
}""", html, count=1)

        # 4. renderDoctorsList calls replacement:
        # Instead of replacing renderDoctorsList, we make fetchDoctors and call it.
        # Let's insert fetchDoctors before renderDoctorsList
        if "async function fetchDoctors" not in html:
            html = html.replace("function renderDoctorsList", 
"""async function fetchDoctors(specialty = "all") {
    try {
        const query = specialty && specialty !== 'all' && specialty !== 'All' ? `?specialty=${specialty}` : '';
        const res = await fetch(`${BASE_URL}/doctors${query}`, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        const docs = await res.json();
        const uiDocs = docs.map(d => ({
            id: d.id, name: d.name, spec_en: d.specialty, spec_ar: d.specialty, spec_tr: d.specialty,
            rating: d.rating, patients: '100+', exp: '10y', emoji: '👨‍⚕️', color: '#d4f5e9', filter: d.specialty
        }));
        renderDoctorsList(uiDocs);
    } catch(e) {
        console.error(e);
    }
}

function renderDoctorsList""")

        # Replace static calls
        html = html.replace("renderDoctorsList(doctorsData)", "fetchDoctors('all')")

        # 5. searchPharmacy
        if "async function searchPharmacy" not in html:
            html = html.replace("function renderMedGrid", 
"""async function searchPharmacy(query) {
    if (!query) query = "panadol";
    try {
        const res = await fetch(`${BASE_URL}/medicines/search?q=${query}`, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        const meds = await res.json();
        const uiMeds = meds.map((m, i) => ({
            id: i + 1, emoji: '💊', name_en: m.brand_name || m.generic_name || 'Medicine',
            name_ar: m.brand_name || 'Medicine', name_tr: m.brand_name || 'Medicine',
            desc_en: (m.purpose || '').substring(0, 50),
            price: `$${(Math.random()*10 + 5).toFixed(2)}`
        }));
        renderMedGrid(uiMeds);
    } catch(e) {
        console.error(e);
    }
}

function renderMedGrid""")

        # 6. Reminder List
        # Replace the whole renderReminderList function
        html = re.sub(r'function renderReminderList\(\)\s*\{[\s\S]*?`\)\.join\(\'\'\);\s*\}',
"""async function fetchReminders() {
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

function renderReminderList() { fetchReminders(); }""", html)

        # 7. Add checkout function replacement
        html = re.sub(r'function checkout\(\)\s*\{[\s\S]*?showToast\(t\(\'toastOrder\'\),\s*\'success\'\);\s*\}', 
"""async function checkout() {
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
}""", html)

        print("New HTML length:", len(html))

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
            
        print("Patched MedLinka.html successfully")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_patch()
