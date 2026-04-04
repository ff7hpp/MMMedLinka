import os
from aiosmtplib import send
from email.message import EmailMessage

BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")

async def send_reminder_email(to_email: str, name: str, medicine: str, dose: str, time: str):
    if not BREVO_SMTP_KEY or not BREVO_SENDER_EMAIL:
        return # Skip if not configured
        
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f0f4f8; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 10px; border-top: 5px solid #12a090;">
            <h2 style="color: #12a090;">MedLinka Reminder</h2>
            <p>Hello {name},</p>
            <p>It's time to take your medicine:</p>
            <div style="background-color: #e8f8f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin: 0; color: #0a5a52;">{medicine}</h3>
                <p style="margin: 5px 0 0 0;"><strong>Dose:</strong> {dose}</p>
                <p style="margin: 5px 0 0 0;"><strong>Time:</strong> {time}</p>
            </div>
            <p>Please remember to mark it as done in the MedLinka app.</p>
            <p style="font-size: 12px; color: #8a9ab0; margin-top: 30px;">
                You are receiving this because you set a reminder in MedLinka.<br>
                <a href="#" style="color: #12a090;">Unsubscribe from these reminders</a>
            </p>
        </div>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["From"] = f"MedLinka <{BREVO_SENDER_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = "⏰ Time to take your medicine"
    msg.set_content("Please view this email in an HTML compatible client.")
    msg.add_alternative(html_content, subtype="html")

    try:
        await send(
            msg,
            hostname="smtp-relay.brevo.com",
            port=587,
            username=BREVO_SENDER_EMAIL,
            password=BREVO_SMTP_KEY,
            start_tls=True
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
