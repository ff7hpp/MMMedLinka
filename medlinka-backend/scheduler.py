from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
from database import SessionLocal
import models
from services.brevo_service import send_reminder_email

scheduler = AsyncIOScheduler()

async def check_reminders():
    # Called every 60 seconds
    now = datetime.now()
    # Format current time to match the stored HH:MM string, assuming 24h format for simplicity,
    # or handle the format used by the frontend (like 08:00 AM)
    current_time_str = now.strftime("%H:%M") 
    current_time_12h = now.strftime("%I:%M %p")

    db = SessionLocal()
    try:
        active_reminders = db.query(models.Reminder).filter(models.Reminder.active == True).all()
        for rem in active_reminders:
            # Basic time match (this can be improved to handle precise ±1min logic depending on frontend time format)
            if rem.time == current_time_str or rem.time.lower() == current_time_12h.lower() or rem.time == now.strftime("%H:%M:%S")[:5]:
                user = db.query(models.User).filter(models.User.id == rem.user_id).first()
                if user:
                    # Fire and forget email
                    asyncio.create_task(
                        send_reminder_email(user.email, user.name, rem.medicine, rem.dose, rem.time)
                    )
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(check_reminders, "interval", seconds=60)
    scheduler.start()
