import requests
from requests import Response

from src.common.config import api_link, api_timeout
from src.common.models import UserDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class RegistrationClient:
    __link = f"{api_link}/users"

    @classmethod
    def signup_user(cls, payload):
        url = f"{cls.__link}/"
        r = requests.post(url, data=payload, timeout=api_timeout)

        return r

    @classmethod
    def get_user(cls, user_id: int) -> ApiResponse[UserDto]:
        url = f"{cls.__link}/{user_id}/"
        response = requests.get(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, UserDto)

    @classmethod
    def apply_for_role(cls, user_id: int, role: str) -> Response:
        url = f"{cls.__link}/{user_id}/apply-role/{role}/"
        r = requests.post(url, timeout=api_timeout)

        return r
