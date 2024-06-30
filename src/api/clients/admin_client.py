import requests
from src.config import api_link


class AdminClient:
    __link = f"{api_link}/admin"

    @classmethod
    def role_requests(cls, role: str):
        url = f"{cls.__link}/role-requests/{role}/"
        r = requests.get(url)

        return r

    @classmethod
    def role_request(cls, role_request_id: int):
        url = f"{cls.__link}/user-requests/{role_request_id}/"
        r = requests.get(url)

        return r

    @classmethod
    def accept_user_request(cls, user_id: int, role: str):
        url = f"{cls.__link}/users/{user_id}/accept-role/{role}/"
        r = requests.put(url)

        return r

    @classmethod
    def decline_user_request(cls, user_id: int):
        url = f"{cls.__link}/users/{user_id}/decline-role/"
        r = requests.put(url)

        return r
