import requests
from typing import Literal
from ..http_client import HTTPClient, ApiResponse

from src.core.config import api_link
from src.core.models import Role, ItemsDto, SubjectDto

from src.bot.src.services.api.api_utils import ApiUtils


class SubjectClient:
    client = HTTPClient("subjects")

    @classmethod
    def get_available_subjects(cls, **kwargs) -> ApiResponse[ItemsDto[SubjectDto]]:
        url = ""

        return cls.client.check_session(**kwargs).get(url, ItemsDto[SubjectDto])

    __link = f"{api_link}/subjects"

    @classmethod
    def get_users_subjects(cls, user_id: int, role: Literal[Role.Student, Role.Tutor], is_available: bool) -> ApiResponse[ItemsDto[SubjectDto]]:
        url = f"{cls.__link}/users/{user_id}/available/{is_available}/?role={role}"
        response = requests.get(url)

        return ApiUtils.create_api_response(response, ItemsDto[SubjectDto])
