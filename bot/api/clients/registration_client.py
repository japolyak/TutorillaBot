import requests
from bot.config import api_link


class RegistrationClient:
    @staticmethod
    def signup_user(payload):
        url = f"{api_link}/users/"
        r = requests.post(url, data=payload)

        return r

    @staticmethod
    def get_user(user_id: int):
        url = f"{api_link}/users/{user_id}/"
        r = requests.get(url)

        return r

    @staticmethod
    def apply_for_role(user_id: int, role: str):
        url = f"{api_link}/users/{user_id}/apply_role/{role}/"
        r = requests.post(url)
        return r
