"""Google OAuth2 authentication module"""
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build


# OAuth2 scopes
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

ALLOWED_USERS = set(
    email.strip()
    for email in os.getenv("ALLOWED_USERS", "").split(",")
    if email.strip()
)

CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("CLIENT_ID"),
        "project_id": os.getenv("PROJECT_ID"),
        "auth_uri": os.getenv("AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.getenv("TOKEN_URI", "https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": os.getenv(
            "AUTH_PROVIDER_X509_CERT_URL",
            "https://www.googleapis.com/oauth2/v1/certs"
        ),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
}


def get_google_flow(redirect_uri: str) -> Flow:
    """Create Google OAuth flow"""
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )


def validate_credentials(creds_data: dict) -> bool:
    """
    Validate a given set of credentials. If the credentials exist, but are
    expired (but have a refresh token), they are refreshed automatically.

    Args:
        creds_data: Dictionary containing credential information

    Returns:
        bool: True if credentials exist and are valid (or refreshed), False otherwise
    """
    creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(GoogleRequest())
                # Update the creds_data in-place with refreshed credentials
                refreshed_data = json.loads(creds.to_json())
                creds_data.update(refreshed_data)
                return True
            except Exception:
                return False
        return False

    return True


def get_user_info(credentials: Credentials) -> dict:
    """
    Get user information from Google API service object (requires valid credentials).

    Args:
        credentials: Google OAuth2 credentials

    Returns:
        dict: User information including email
    """
    service = build('oauth2', 'v2', credentials=credentials)
    return service.userinfo().get().execute()


def is_user_allowed(email: str) -> bool:
    """
    Check if user email is in the allowed users list.

    Args:
        email: User's email address

    Returns:
        bool: True if user is allowed, False otherwise
    """
    return email in ALLOWED_USERS
