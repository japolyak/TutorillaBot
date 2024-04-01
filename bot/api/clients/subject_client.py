import requests
from bot.config import api_link


class SubjectClient:
    __link = f"{api_link}/subjects"

    @classmethod
    def get_available_subjects(cls, user_id: int, role: str):
        url = f"{cls.__link}/available-subjects/users/{user_id}/?role={role}"
        r = requests.get(url)

        return r

    @classmethod
    def get_users_subjects(cls, user_id: int, role: str):
        url = f"{cls.__link}/users/{user_id}/?role={role}"
        r = requests.get(url)

        return r
