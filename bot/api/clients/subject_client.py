import requests
from bot.config import api_link


class SubjectClient:
    @staticmethod
    def get_available_subjects(user_id: int, role: str):
        url = f"{api_link}/subjects/available-subjects/users/{user_id}/?role={role}"
        r = requests.get(url)

        return r

    @staticmethod
    def get_users_subjects(user_id: int, role: str):
        url = f"{api_link}/subjects/users/{user_id}/?role={role}"
        r = requests.get(url)

        return r
