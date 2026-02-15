"""
Authentication module for Google OAuth2

Exports the main components needed for authentication:
    - router: FastAPI router with auth endpoints
    - AuthMiddleware: Middleware for protecting routes
    - session_manager: Global session manager instance
"""

from .router import router
from .middleware import AuthMiddleware
from .session_manager import session_manager

__all__ = ["router", "AuthMiddleware", "session_manager"]
