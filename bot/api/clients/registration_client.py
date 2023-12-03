import requests
from bot.config import api_link


class RegistrationClient:
    @staticmethod
    def signup_user(payload):
        url = f"{api_link}/signup/"
        r = requests.post(url, data=payload)

        return r

    @staticmethod
    def get_user(user_id: int):
        url = f"{api_link}/user/{user_id}/"
        r = requests.get(url)

        return r

    @staticmethod
    def apply_for_tutor_role(user_id: int):
        url = f"{api_link}/user/{user_id}/tutor/"
        r = requests.put(url)

        return r

    @staticmethod
    def apply_for_student_role(user_id: int):
        url = f"{api_link}/user/{user_id}/student/"
        r = requests.put(url)
        return r
