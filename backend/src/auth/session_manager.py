class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id, credentials):
        self.sessions[user_id] = credentials

    def get_session(self, user_id):
        return self.sessions.get(user_id)

    def delete_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
