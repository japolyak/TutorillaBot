from ..http_client import HTTPClient

from src.common.models import UserDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class UserClient:
    client = HTTPClient("users")

    @classmethod
    def get_user(cls, user_id: int, **kwargs) -> ApiResponse[UserDto]:
        response = cls.client.check_session(**kwargs).get(f"{user_id}/")

        return ApiUtils.create_api_response(response, UserDto)
