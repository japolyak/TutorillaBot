import requests
from typing import Literal

from src.common.config import api_link, api_timeout
from src.common.models import Role, ItemsDto, SubjectDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class SubjectClient:
    __link = f"{api_link}/subjects"

    @classmethod
    def get_users_subjects(cls, user_id: int, role: Literal[Role.Student, Role.Tutor], is_available: bool) -> ApiResponse[ItemsDto[SubjectDto]]:
        url = f"{cls.__link}/users/{user_id}/available/{is_available}/?role={role}"
        response = requests.get(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, ItemsDto[SubjectDto])
