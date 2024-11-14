import requests

from src.common.config import api_link, api_timeout
from src.common.models import UserDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class AdminClient:
    __link = f"{api_link}/admin"

    @classmethod
    def accept_user_request(cls, user_id: int, role: str) -> ApiResponse[UserDto]:
        url = f"{cls.__link}/users/{user_id}/accept-role/{role}/"
        response = requests.put(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, UserDto)
