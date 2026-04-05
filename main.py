import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routers import auth_router, chat_router, doctors_router, pharmacy_router, reminders_router
from scheduler import start_scheduler

# إنشاء جداول قاعدة البيانات
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler() 
    print("🚀 MedLinka Backend is LIVE!")
    yield
    print("🛑 MedLinka is shutting down.")

app = FastAPI(title="MedLinka API", lifespan=lifespan)

# --- إعدادات الملفات (السر في ظهور التصميم) ---
# تأكد من وجود مجلد اسمه static في نفس المجلد وضع فيه ملفات الـ CSS والصور
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# المسار الرئيسي لعرض الواجهة
@app.get("/")
async def serve_frontend():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MedLinka.html")
    return FileResponse(file_path)

# تضمين المسارات
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(doctors_router.router)
app.include_router(pharmacy_router.router)
app.include_router(reminders_router.router)

if __name__ == "__main__":
    import uvicorn
    # السر هنا: تغيير الـ host إلى 0.0.0.0 ليراه الجوال
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)