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

## AWS Free Tier deployment

For an account eligible for the AWS Free Tier, the lowest-cost setup is one EC2
instance running both services. Free Tier eligibility, limits, and pricing vary
by account creation date and region; add a billing alarm before starting.

1. Launch an Ubuntu EC2 `t2.micro` or `t3.micro` instance and allow inbound SSH
   (port 22) and HTTP (port 80). Use HTTPS (port 443) after installing a
   certificate. A public IPv4 address can incur a charge, so check the current
   EC2 pricing for your region.
2. Install Python, Node.js, Nginx, and Git. Clone this repository onto the
   instance.
3. Start FastAPI on `127.0.0.1:8000` with systemd. Do not expose port 8000
   publicly.
4. Build the frontend with `npm run build -- --configuration production`.
5. Configure Nginx to serve
   `frontend/dist/social-description-extractor/browser/` and proxy `/api/` to
   `http://127.0.0.1:8000/api/`. The production Angular API URL is relative,
   so no App Runner URL needs to be committed.
6. Set `ALLOWED_ORIGINS` to the website origin if you keep CORS enabled, then
   use Certbot/Let's Encrypt for HTTPS.

Do not commit AWS credentials. Use an IAM role with only the permissions
needed. Instagram and YouTube can restrict automated requests, and scraping
must comply with their terms. AWS free-tier allowances are limited and may
expire, so monitor Billing and set a zero-spend budget alert.
