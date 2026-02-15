import os
import json
import secrets
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build


# Load environment variables from .env file if not in production
if os.getenv("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()


app = FastAPI(title="Leaflet WebApp Backend", version="1.0.0")

# Serve static files from the frontend build (dist) directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "frontend" / "dist" / "frontend" / "browser"


# Parse allowed users from environment variable
ALLOWED_USERS = set(
    email.strip()
    for email in os.getenv("ALLOWED_USERS", "").split(",")
    if email.strip()
)

# Build client config from environment variables
client_config = {
    "web": {
        "client_id": os.getenv("CLIENT_ID"),
        "project_id": os.getenv("PROJECT_ID"),
        "auth_uri": os.getenv("AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.getenv("TOKEN_URI", "https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
}

# OAuth2 scopes
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"]

# Store sessions (in production, use Redis or database)
sessions = {}

# Public paths that don't require authentication
PUBLIC_PATHS = {"/api/login", "/api/auth/callback"}


def get_google_flow(redirect_uri: str):
    """Create Google OAuth flow"""
    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )


def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated"""
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in sessions:
        return False

    creds_data = sessions[session_id]
    creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    # Check if credentials are valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(GoogleRequest())
                sessions[session_id] = json.loads(creds.to_json())
                return True
            except:
                return False
        return False

    return True


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to redirect unauthenticated users to login"""

    async def dispatch(self, request: Request, call_next):
        # Skip auth check for public paths
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Check if user is authenticated
        if not is_authenticated(request):
            # Redirect to login
            return RedirectResponse(url="/api/login")

        response = await call_next(request)
        return response


# Add auth middleware
app.add_middleware(AuthMiddleware)


@app.get("/api/login")
async def login(request: Request):
    """Initiate OAuth flow"""
    redirect_uri = str(request.url_for("oauth_callback"))
    flow = get_google_flow(redirect_uri)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    # Store state for CSRF protection
    sessions[f"state_{state}"] = {"state": state}

    response = RedirectResponse(authorization_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True, max_age=600)
    return response


@app.get("/api/auth/callback")
async def oauth_callback(request: Request, code: str, state: str):
    """Handle OAuth callback"""
    stored_state = request.cookies.get("oauth_state")

    if state != stored_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    redirect_uri = str(request.url_for("oauth_callback"))
    flow = get_google_flow(redirect_uri)

    flow.fetch_token(code=code)
    credentials = flow.credentials

    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    user_email = user_info.get('email')

    if user_email not in ALLOWED_USERS:
        raise HTTPException(status_code=403, detail="Access denied. User not authorized.")


    # Create session
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = json.loads(credentials.to_json())

    # Clean up state
    sessions.pop(f"state_{state}", None)

    # Redirect to frontend with session cookie
    response = RedirectResponse(url="/")
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=86400, samesite="lax")
    response.delete_cookie(key="oauth_state")

    return response


@app.get("/api/logout")
async def logout(request: Request):
    """Logout user"""
    session_id = request.cookies.get("session_id")
    if session_id:
        sessions.pop(session_id, None)

    response = RedirectResponse(url="/api/login")
    response.delete_cookie(key="session_id")
    return response


@app.get("/api/status")
def status():
    return {"status": "online"}


app.mount("/", StaticFiles(directory=ASSETS_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
