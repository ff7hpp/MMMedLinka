# MedLinka Deployment Guide (Railway)

### Step 1: Push to GitHub
1. Validate that your `.gitignore` correctly ignores `.env`.
2. Commit your code and push it to a new GitHub repository.

### Step 2: Railway Setup
1. Log into your [Railway account](https://railway.app/).
2. Create a new Project -> **Deploy from GitHub repo**.
3. Select the repository you just created.

### Step 3: Environment Variables
Go to **Variables** tab on Railway and configure:
- `GOOGLE_API_KEY`: Your Google Gemini API key (get it from [aistudio.google.com](https://aistudio.google.com/app/apikey))
- `WOLFRAM_APP_ID`: Your WolframAlpha App ID
- `BREVO_SMTP_KEY`: Your Brevo SMTP API Key
- `BREVO_SENDER_EMAIL`: Your configured Brevo verified email address
- `OPENFDA_API_KEY`: (Optional) Your OpenFDA key
- `JWT_SECRET`: Use the value already set in your `.env` file
- `DATABASE_URL`: `sqlite:///./medlinka.db`

### Step 4: Setup Procfile
By default, Railway automatically detects Python using the `requirements.txt`.
Create a `Procfile` at the root of `medlinka-backend` with the following content:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Frontend Updates
In your `MedLinka.html` frontend file:
1. Update `BASE_URL`:
   Change:
   `const BASE_URL = "http://localhost:8000/api";`
   To:
   `const BASE_URL = "https://your-railway-app-url.up.railway.app/api";`
2. Save, then open `MedLinka.html` directly in the browser, or host it on GitHub Pages.

### AI Provider
This app uses **Google Gemini 1.5 Flash** via the `google-generativeai` SDK.
- Service file: `services/gemini_service.py`
- Model: `gemini-1.5-flash`
- Env var: `GOOGLE_API_KEY`

