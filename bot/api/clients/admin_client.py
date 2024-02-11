import requests
from bot.config import api_link


class AdminClient:
    @staticmethod
    def role_requests(role: str):
        url = f"{api_link}/admin/role-requests/{role}/"
        r = requests.get(url)

        return r

    @staticmethod
    def role_request(role_request_id: int):
        url = f"{api_link}/admin/user-requests/{role_request_id}/"
        r = requests.get(url)

        return r

    @staticmethod
    def accept_user_request(user_id: int, role: str):
        url = f"{api_link}/admin/users/{user_id}/accept-role/{role}/"
        r = requests.put(url)

        return r

    @staticmethod
    def decline_user_request(user_id: int):
        url = f"{api_link}/admin/users/{user_id}/decline-role/"
        r = requests.put(url)

        return r
