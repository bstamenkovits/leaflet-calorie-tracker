"""Authentication middleware to protect routes"""
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth.session_manager import session_manager
from auth.oauth import validate_credentials


# Public paths that don't require authentication
PUBLIC_PATHS = {"/api/login", "/api/auth/callback"}


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to redirect unauthenticated users to login endpoint.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Default dispatch method for the middleware, should be overwritten for
        any custom BaseHTTPMiddleware implementations. This method is called for
        each incoming request, and is responsible for processing the request and
        returning a response.

        In this case the dispatch method checks if the request is for a public
        path (i.e. a path that doesn't require authentication), and if not, it
        checks if the user is authenticated. If the user is not authenticated,
        they are redirected to the login page.

        Args:
            request: The incoming HTTP request
            call_next: A function that takes a request and returns a response, used to call the next middleware or route handler in the chain

        Returns:
            Response: The HTTP response to be sent back to the client
        """
        # skip auth check for public paths (e.g. login and callback endpoints)
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # redirect unauthenticated users to login page
        if not self._is_authenticated(request):
            return RedirectResponse(url="/api/login")

        response = await call_next(request)
        return response

    def _is_authenticated(self, request: Request) -> bool:
        """
        Check if user is authenticated

        When a user logs in, their credentials are stored in the session manager
        with a unique session ID. The session ID is stored in a cookie on the
        client side. For each incoming request, the middleware checks for the
        session ID cookie, retrieves the corresponding credentials from the
        session manager, and validates them.

        

        Args:
            request: The incoming HTTP request
        Returns:
            bool: True if the user is authenticated, False otherwise
        """
        session_id = request.cookies.get("session_id")

        if not session_id:
            return False

        creds_data = session_manager.get_session(session_id)
        if not creds_data:
            return False

        # Validate credentials (will refresh if needed)
        return validate_credentials(creds_data)
