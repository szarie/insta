# Social Description Extractor

Angular frontend and FastAPI backend for extracting descriptions from public Instagram and YouTube links.

## Run locally

Backend:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --reload --port 8000
```

Frontend (requires Node.js and Angular CLI dependencies):

```powershell
cd frontend
npm install
npm start
```

Open `http://localhost:4200`. Only public URLs are supported. Platform metadata and automated access can change, so unavailable pages are reported explicitly.
