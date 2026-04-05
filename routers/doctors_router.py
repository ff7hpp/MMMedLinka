from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db, engine
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/api", tags=["Doctors & Appointments"])

# Seed function
def seed_doctors(db: Session):
    if db.query(models.Doctor).first() is None:
        sample_doctors = [
            {"name": "Dr. Ahmed Mohamed", "specialty": "General", "rating": 4.9, "bio": "Experienced general practitioner."},
            {"name": "Dr. Sara Ali", "specialty": "Cardiology", "rating": 4.8, "bio": "Expert in cardiovascular health."},
            {"name": "Dr. Khalid Ibrahim", "specialty": "Pediatrics", "rating": 4.9, "bio": "Friendly and experienced pediatric doctor."},
            {"name": "Dr. Mona Hassan", "specialty": "Dermatology", "rating": 4.7, "bio": "Specialist in skin care and dermatological conditions."},
            {"name": "Dr. Omar Yousuf", "specialty": "Eye Care", "rating": 4.8, "bio": "Ophthalmologist with 15 years experience."},
            {"name": "Dr. Fatima Omar", "specialty": "General", "rating": 4.6, "bio": "Compassionate general health care provider."},
            {"name": "Dr. Youssef Kamel", "specialty": "Orthopedics", "rating": 4.5, "bio": "Specializes in bone and joint health."},
            {"name": "Dr. Layla Mahmoud", "specialty": "Neurology", "rating": 4.9, "bio": "Expert in neurological disorders."},
            {"name": "Dr. Tarek Mostafa", "specialty": "Cardiology", "rating": 4.7, "bio": "Focuses on heart rhythm disorders."},
            {"name": "Dr. Huda Samir", "specialty": "Pediatrics", "rating": 4.8, "bio": "Dedicated to child health and development."}
        ]
        db.bulk_insert_mappings(models.Doctor, sample_doctors)
        db.commit()

# Seed doctors on first run (called at module import time)
with Session(engine) as _db:
    seed_doctors(_db)

@router.get("/doctors")
def get_doctors(specialty: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Doctor)
    if specialty and specialty.lower() != "all":
        query = query.filter(models.Doctor.specialty.ilike(f"%{specialty}%"))
    return query.all()

@router.post("/appointments/book", response_model=schemas.AppointmentOut)
def book_appointment(appt: schemas.AppointmentCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validate slot
    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appt.doctor_id,
        models.Appointment.date == appt.date,
        models.Appointment.time == appt.time,
        models.Appointment.status != "Cancelled"
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Time slot already booked")
        
    new_appt = models.Appointment(
        user_id=current_user.id,
        doctor_id=appt.doctor_id,
        date=appt.date,
        time=appt.time,
        reason=appt.reason
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    return new_appt

@router.get("/appointments/my", response_model=List[schemas.AppointmentOut])
def get_my_appointments(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id).all()

@router.delete("/appointments/{appt_id}")
def cancel_appointment(appt_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this appointment")
        
    appt.status = "Cancelled"
    db.commit()
    return {"detail": "Appointment cancelled successfully"}
