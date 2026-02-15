"""Authentication router with login, callback, and logout endpoints"""
import json
import secrets
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from auth.oauth import get_google_flow, get_user_info, is_user_allowed
from auth.session_manager import session_manager


router = APIRouter(prefix="/api", tags=["auth"])


@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    """
    Initiate OAuth flow.

    The google OAuth flow includes a "state" parameter that is used for CSRF (
    Cross-Site Request Forgery) protection.

    This state is generated when the flow is initiated and stored in the session
    manager. When Google redirects back to the callback endpoint, it includes the
    same state parameter. The callback handler checks if the received state
    matches the stored state.

    If they don't match, it means the request might be forged or tampered with, and
    the authentication process is aborted.

        * Prevents attackers from initiating an OAuth flow on their end and
          tricking users into authenticating with the attacker's app instead of
          this one
        * Ensures the callback response corresponds to the same login request
          that originated from this application, not some malicious third party
          application
        * If the states don't match, it means someone tampered with the flow or
          it's a malicious callback

    Args:
        request: FastAPI request object
    Returns:
        RedirectResponse: response from the redirect server
    """

    # create a google OAuth flow instance with the appropriate redirect URI
    redirect_uri = str(request.url_for("oauth_callback"))
    flow = get_google_flow(redirect_uri)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    # redirect user to Google's OAuth 2.0 server
    response = RedirectResponse(authorization_url)

    # store the state in the session manager for later validation
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True, # prevent client-side scripts (e.g., JavaScript) from accessing the cookie; XSS attack mitigation
        max_age=600,
        secure=True, # ensure cookie is only sent over HTTPS
    )
    return response


@router.get("/auth/callback")
async def oauth_callback(request: Request, code: str, state: str) -> RedirectResponse:
    """
    Handle OAuth callback

    After the user authenticates with Google, they are redirected back to this
    endpoint with a code and state parameter. The code is exchanged for access
    tokens, and the state is validated to ensure the request is legitimate.

    State:
    The state parameter is generated prior to the user logging in, and is stored
    inside of a cookie. This is compared to the state parameter received from
    Google in the callback request.

    Session:
    If the state is valid, a session is created for the user. The session ID is
    stored in a cookie, and the user's credentials are stored in the session
    manager. This allows the user to remain authenticated for subsequent
    requests (see ).
    """
    # get stored state from cookie and compare with the state received from Google
    stored_state = request.cookies.get("oauth_state")

    if state != stored_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    # obtain tokens using the authorization code provided by Google after user consent
    redirect_uri = str(request.url_for("oauth_callback"))
    flow = get_google_flow(redirect_uri)
    flow.fetch_token(code=code)

    # get user info from Google using the obtained credentials
    credentials = flow.credentials
    user_info = get_user_info(credentials)
    user_email = user_info.get('email')

    # check if user is authorized to access the app
    if not is_user_allowed(user_email):
        raise HTTPException(status_code=403, detail="Access denied. User not authorized.")

    # Create session
    session_id = secrets.token_urlsafe(32)
    credentials_data = json.loads(credentials.to_json())
    session_manager.create_session(session_id, credentials_data)

    # Clean up OAuth state
    session_manager.delete_oauth_state(state)

    # Redirect to frontend with session cookie
    response = RedirectResponse(url="/")
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=86400, samesite="lax")
    response.delete_cookie(key="oauth_state")

    return response


@router.get("/logout")
async def logout(request: Request):
    """Logout user"""
    session_id = request.cookies.get("session_id")
    if session_id:
        session_manager.delete_session(session_id)

    response = RedirectResponse(url="/api/login")
    response.delete_cookie(key="session_id")
    return response
