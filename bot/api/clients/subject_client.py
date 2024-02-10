import requests
from bot.config import api_link


class SubjectClient:
    @staticmethod
    def get_classes(user_id: int, role: str):
        url = f"{api_link}/subjects/users/{user_id}/?role={role}"
        r = requests.get(url)

        return r
