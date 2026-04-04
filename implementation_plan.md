# 🔍 PHASE 0 — ARCHITECTURE PLAN

## Goal Description
Build a complete, production-ready backend for MedLinka — a mobile health application with 5 core modules. The backend will replace all mock/static data with real API calls, DB persistence, and 3rd-party services using FastAPI and SQLite, with deployment readiness for platforms like Railway.

## 📁 Full project folder structure:
```text
medlinka-backend/
├── main.py                  ← FastAPI app entry point
├── .env                     ← ALL secrets (never commit this)
├── .gitignore               ← must include .env
├── requirements.txt         ← all pip dependencies
├── database.py              ← SQLAlchemy setup + Base
├── models.py                ← all DB table models
├── schemas.py               ← all Pydantic request/response schemas
├── auth.py                  ← JWT logic + password hashing
├── scheduler.py             ← APScheduler for reminders
└── routers/
    ├── auth_router.py       ← /api/auth/*
    ├── home_router.py       ← /api/home/*
    ├── chat_router.py       ← /api/chat/*
    ├── doctors_router.py    ← /api/doctors/* + /api/appointments/*
    ├── pharmacy_router.py   ← /api/medicines/* + /api/orders/*
    └── reminders_router.py  ← /api/reminders/*
└── services/
    ├── groq_service.py      ← Groq API wrapper
    ├── wolfram_service.py   ← WolframAlpha API wrapper
    ├── brevo_service.py     ← Brevo SMTP email sender
    └── openfda_service.py   ← OpenFDA drug search wrapper
```

## 📊 Database Tables:
| Table          | Key Columns                                      |
|----------------|--------------------------------------------------|
| users          | id, name, email, hashed_password, created_at    |
| doctors        | id, name, specialty, rating, bio, available      |
| appointments   | id, user_id, doctor_id, date, time, reason,status|
| reminders      | id, user_id, medicine, dose, time, frequency,active|
| orders         | id, user_id, items_json, total, status,created_at|
| chat_history   | id, user_id, role, message, timestamp            |

## 🔗 API Endpoints Master List:
| Method | Endpoint                    | Auth? | Module      |
|--------|-----------------------------|-------|-------------|
| POST   | /api/auth/register          | No    | Auth        |
| POST   | /api/auth/login             | No    | Auth        |
| GET    | /api/auth/me                | Yes   | Auth        |
| GET    | /api/home/summary           | Yes   | Home        |
| POST   | /api/chat/send              | Yes   | AI Chat     |
| GET    | /api/doctors                | Yes   | Doctors     |
| POST   | /api/appointments/book      | Yes   | Doctors     |
| GET    | /api/appointments/my        | Yes   | Doctors     |
| DELETE | /api/appointments/{id}      | Yes   | Doctors     |
| GET    | /api/medicines/search       | Yes   | Pharmacy    |
| POST   | /api/orders/place           | Yes   | Pharmacy    |
| GET    | /api/orders/my              | Yes   | Pharmacy    |
| GET    | /api/reminders              | Yes   | Reminders   |
| POST   | /api/reminders              | Yes   | Reminders   |
| PUT    | /api/reminders/{id}         | Yes   | Reminders   |
| DELETE | /api/reminders/{id}         | Yes   | Reminders   |

## User Review Required
Architecture approved? Shall I begin Phase 1 — Core Setup?
