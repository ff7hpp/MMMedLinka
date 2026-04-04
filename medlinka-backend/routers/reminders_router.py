from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])

@router.get("", response_model=List[schemas.ReminderOut])
def get_reminders(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Reminder).filter(models.Reminder.user_id == current_user.id).all()

@router.post("", response_model=schemas.ReminderOut)
def create_reminder(rem: schemas.ReminderCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_rem = models.Reminder(
        user_id=current_user.id,
        medicine=rem.medicine,
        dose=rem.dose,
        time=rem.time,
        frequency=rem.frequency,
        active=True
    )
    db.add(new_rem)
    db.commit()
    db.refresh(new_rem)
    return new_rem

@router.put("/{rem_id}", response_model=schemas.ReminderOut)
def update_reminder(rem_id: int, rem: schemas.ReminderCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(models.Reminder).filter(models.Reminder.id == rem_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if existing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    existing.medicine = rem.medicine
    existing.dose = rem.dose
    existing.time = rem.time
    existing.frequency = rem.frequency
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{rem_id}")
def delete_reminder(rem_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(models.Reminder).filter(models.Reminder.id == rem_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if existing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.delete(existing)
    db.commit()
    return {"detail": "Reminder deleted successfully"}
