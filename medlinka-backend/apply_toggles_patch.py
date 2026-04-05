import re

def apply_toggles_patch():
    file_path = "../MedLinka.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        html = re.sub(r'async function toggleRem[\s\S]*?\}',
"""async function toggleRem(id, cb) {
    try {
        const res = await fetch(`${BASE_URL}/reminders/${id}`, {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${currentToken}`
            },
            body: JSON.stringify({
                active: cb.checked
            })
        });
        if (res.ok) showToast(t('toastToggle'), 'success');
    } catch(e) {}
}""", html)

        html = re.sub(r'function addReminder\(\)\s*\{[\s\S]*?showToast\(t\(\'toastRem\'\),\s*\'success\'\);\s*\}',
"""async function addReminder() {
  const i = remCounter % newRemNames.length;
  try {
      const res = await fetch(`${BASE_URL}/reminders`, {
          method: "POST",
          headers: { 
              "Content-Type": "application/json",
              "Authorization": `Bearer ${currentToken}`
          },
          body: JSON.stringify({
              medicine: newRemNames[i],
              dose: '1 pill',
              time: '08:00',
              frequency: 'Once daily'
          })
      });
      if (res.ok) {
          remCounter++;
          fetchReminders();
          showToast(t('toastRem'), 'success');
      }
  } catch(e) {}
}""", html)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_toggles_patch()
