class MemorySessionHandler:
    def __init__(self):
        self.cache = {}

    def get_session(self, user_id: str) -> dict:
        session = self.cache.get(user_id, {})
        return session

    def set_session(self, user_id: str, data: dict):
        self.cache[user_id] = data


session_store = MemorySessionHandler()
