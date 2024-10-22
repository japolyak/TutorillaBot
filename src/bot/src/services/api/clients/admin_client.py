import requests

from src.common.config import api_link, api_timeout
from src.common.models import ItemsDto, UserRequestDto, UserDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class AdminClient:
    __link = f"{api_link}/admin"

    @classmethod
    def role_requests(cls, role: str) -> ApiResponse[ItemsDto[UserRequestDto]]:
        url = f"{cls.__link}/role-requests/{role}/"
        response = requests.get(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, ItemsDto[UserRequestDto])

    @classmethod
    def role_request(cls, role_request_id: int) -> ApiResponse[UserRequestDto]:
        url = f"{cls.__link}/user-requests/{role_request_id}/"
        response = requests.get(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, UserRequestDto)

    @classmethod
    def accept_user_request(cls, user_id: int, role: str) -> ApiResponse[UserDto]:
        url = f"{cls.__link}/users/{user_id}/accept-role/{role}/"
        response = requests.put(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, UserDto)

    @classmethod
    def decline_user_request(cls, user_id: int):
        url = f"{cls.__link}/users/{user_id}/decline-role/"
        response = requests.put(url, timeout=api_timeout)

        return response
