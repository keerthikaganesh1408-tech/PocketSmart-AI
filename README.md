# PocketSmart AI

AI-powered budget and recommendation assistant based on the supplied PocketSmart documentation.

## Features
- Landing page
- Register/login/logout
- JWT cookie authentication
- Dashboard
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner
- Optional outfit-image analysis for jewelry planning
- Gemini AI recommendations
- SQLite recommendation history
- Recommendation detail pages
- Responsive UI

## Run in VS Code (Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put your Gemini API key in `.env`, then:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Never commit `.env` or your API key. The `.gitignore` already excludes it.

## GitHub

```powershell
git init
git add .
git commit -m "Initial PocketSmart AI project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
