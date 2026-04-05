# MedLinka

MedLinka is an AI-powered healthcare assistant application designed to streamline patient-doctor interaction, handle appointment scheduling, manage medication reminders, and provide reliable, AI-driven medical assistance.

## Features

- **AI-Powered Chat:** Interactive medical assistant powered by Google Gemini and Wolfram Alpha for verified factual health responses.
- **Find a Doctor & Book Appointments:** Browse an available list of doctors, filter by specialties, and book appointments directly.
- **Interactive Reminders:** Set active reminders for medication doses with automated email notifications via Brevo.
- **Authentication:** Secure user registration, login, and JWT-based session management.
- **Pharmacy (Coming soon or WIP):** Functionality for medical supplies and pharmacy items.

## Technologies Used

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **AI Integration:** Google Generative AI (Gemini 1.5 Flash), Wolfram Alpha API
- **Authentication:** bcrypt, python-jose (JWT)
- **Background Tasks:** APScheduler for automated reminders
- **Email Delivery:** Brevo SMTP via aiosmtplib

## Environment Variables (.env)

Create a `.env` file in the root directory (was `medlinka-backend/.env`) with the following keys. **Do not commit these to version control.**

```env
GOOGLE_API_KEY=your_gemini_api_key
WOLFRAM_APP_ID=your_wolfram_app_id
BREVO_SMTP_KEY=your_brevo_smtp_key
BREVO_SENDER_EMAIL=your_verified_brevo_sender_email
OPENFDA_API_KEY=your_openfda_api_key
JWT_SECRET=your_secret_key_for_jwt
DATABASE_URL=sqlite:///./medlinka.db
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd MedLinka
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # For Windows:
   .venv\Scripts\activate
   # For Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application locally:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Open in your browser:**
   Navigate to `http://localhost:8000` to view the frontend interface.

## Deployment Notes

- For Heroku or similar PaaS, the `Procfile` is already configured:
  ```
  web: uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- Make sure to define the `.env` variables in your hosting provider's environment settings.
