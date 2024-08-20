import requests
from requests import Response

from src.common.config import api_link


class RegistrationClient:
    __link = f"{api_link}/users"

    @classmethod
    def signup_user(cls, payload):
        url = f"{cls.__link}/"
        r = requests.post(url, data=payload, timeout=15)

        return r

    @classmethod
    def get_user(cls, user_id: int):
        url = f"{cls.__link}/{user_id}/"
        r = requests.get(url, timeout=15)

        return r

    @classmethod
    def apply_for_role(cls, user_id: int, role: str) -> Response:
        url = f"{cls.__link}/{user_id}/apply-role/{role}/"
        r = requests.post(url, timeout=15)
        return r
