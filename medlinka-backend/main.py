import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth_router, chat_router, doctors_router, pharmacy_router, reminders_router
from scheduler import start_scheduler

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# 1. Define the Lifespan Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: This runs when the server starts
    start_scheduler() 
    print("MedLinka scheduler started successfully.")
    
    yield # The application handles requests here
    
    # Shutdown logic: (Optional) You can add cleanup code here
    print("MedLinka services are shutting down.")

# 2. Initialize FastAPI with the lifespan handler
app = FastAPI(
    title="MedLinka API", 
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to MedLinka API"}

app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(doctors_router.router)
app.include_router(pharmacy_router.router)
app.include_router(reminders_router.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)