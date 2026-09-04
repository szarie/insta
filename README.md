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

## AWS deployment

The simplest production setup is:

1. Deploy `backend/` as an AWS App Runner service from this repository. App Runner can build the included `backend/Dockerfile`; use port `8000`, and set `ALLOWED_ORIGINS` to your CloudFront/S3 website URL.
2. Copy the App Runner HTTPS service URL into `frontend/src/environments/environment.production.ts` as `apiUrl`.
3. Build the frontend with `npm run build`; upload `frontend/dist/social-description-extractor/browser/` to an S3 bucket configured for static website hosting, and put CloudFront in front of it.
4. Add the CloudFront URL to App Runner's `ALLOWED_ORIGINS` value and redeploy the backend.

Do not commit AWS credentials. Use an IAM user/role with only the permissions needed for the selected deployment. Public scraping can be restricted by Instagram or YouTube and must comply with their terms.
