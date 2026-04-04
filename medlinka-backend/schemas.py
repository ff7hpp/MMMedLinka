from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Auth ---
class RegisterForm(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginForm(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    token: str
    user: UserProfile

# --- Chat ---
class ChatMessage(BaseModel):
    message: str

# --- Appointments ---
class AppointmentCreate(BaseModel):
    doctor_id: int
    date: str
    time: str
    reason: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    date: str
    time: str
    status: str
    
    class Config:
        from_attributes = True

# --- Reminders ---
class ReminderCreate(BaseModel):
    medicine: str
    dose: str
    time: str
    frequency: str

class ReminderOut(BaseModel):
    id: int
    medicine: str
    dose: str
    time: str
    frequency: str
    active: bool
    
    class Config:
        from_attributes = True

# --- Orders ---
class OrderItem(BaseModel):
    name: str
    qty: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: int
    items_json: str
    total: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
