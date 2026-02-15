"""Session manager for handling user sessions and OAuth state"""


class SessionManager:
    """
    Class to manage user sessions and OAuth state. In production, this should be
    replaced with Redis or a database, but for simplicity of this hobby project
    a simple in-memory dictionary is used.

    Note that this means sessions will be lost when the server restarts, which
    is acceptable for this use case.
    """

    def __init__(self):
        self.sessions = {}
        self.oauth_states = {}

    def create_session(self, session_id: str, credentials: dict) -> None:
        """
        Create a new session with user credentials

        Args:
            session_id: Unique session identifier
            credentials: User's OAuth credentials as a dictionary
        """
        self.sessions[session_id] = credentials

    def get_session(self, session_id: str) -> dict | None:
        """
        Get session data by session ID

        Args:
            session_id: Unique session identifier

        Returns:
            User credentials dict or None if session doesn't exist
        """
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session

        Args:
            session_id: Unique session identifier
        """
        self.sessions.pop(session_id, None)

    def store_oauth_state(self, state: str) -> None:
        """
        Store OAuth state for CSRF protection

        Args:
            state: OAuth state parameter
        """
        self.oauth_states[f"state_{state}"] = {"state": state}

    def delete_oauth_state(self, state: str) -> None:
        """
        Delete OAuth state after successful callback

        Args:
            state: OAuth state parameter
        """
        self.oauth_states.pop(f"state_{state}", None)



"""
Store a global instance of the session manager to be used across the application.

Python modules are singletons, so this instance will be shared wherever it's
imported: python stores imported modules in sys.modules, and only runs them on
the first import. All subsequent imports will reference the same module object,
and thus the same instance of the session manager.
"""
session_manager = SessionManager()
