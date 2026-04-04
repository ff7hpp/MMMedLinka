import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth_router, chat_router, doctors_router, pharmacy_router, reminders_router
from scheduler import start_scheduler

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedLinka API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to MedLinka API"}

app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(doctors_router.router)
app.include_router(pharmacy_router.router)
app.include_router(reminders_router.router)
