from ..http_client import HTTPClient, ApiResponse

from src.common.models import UserDto


class UserClient:
    client = HTTPClient("users")

    @classmethod
    def get_user(cls, **kwargs) -> ApiResponse[UserDto]:
        url = "me/"

        return cls.client.check_session(**kwargs).get(url, UserDto)

    @classmethod
    def signup_user(cls, payload, **kwargs) -> ApiResponse[None]:
        return cls.client.check_session(**kwargs).post("", None, data=payload)

    @classmethod
    def apply_for_role(cls, role: str, **kwargs) -> ApiResponse[None]:
        url = f"apply-role/{role}/"

        return cls.client.check_session(**kwargs).post(url, None)
