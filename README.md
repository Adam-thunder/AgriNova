# AgriDoctor — SIH Demo


This repo contains a simple FastAPI backend and static frontend for your SIH demo.


## Quick setup (local)


1. Clone repo.
2. Backend:
- cd backend
- python -m venv .venv
- source .venv/bin/activate # (Linux/mac)
- pip install -r requirements.txt
- export OPENWEATHER_KEY=your_openweather_key
- uvicorn app:app --host 0.0.0.0 --port 8000
3. Frontend: Serve `frontend/` (you can use `npx serve` or simply deploy static files).


## Deployment (recommended for SIH)


- Push the repo to GitHub.
- Deploy backend on Render or Railway (follow their FastAPI guides). Set environment variables there (OPENWEATHER_KEY). The AI key is currently embedded in backend/app.py as requested — for production move it to env var `AI_API_KEY`.
- Deploy frontend on Vercel or Netlify and set the backend URL in `script.js` (or host frontend on the same domain if using Render's static si