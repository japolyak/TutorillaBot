from requests import get

from src.core.config import api_link
from src.core.models import PaginatedList, PrivateClassDto, ItemsDto, PrivateCourseInlineDto
from ..http_client import ApiResponse

from src.bot.src.services.api.api_utils import ApiUtils


class PrivateCourseClient:
    __link = f"{api_link}/private-courses"

    @classmethod
    def get_private_courses_by_course_name(cls, user_id: int, subject_name: str, role: str) -> ApiResponse[ItemsDto[PrivateCourseInlineDto]]:
        url = f"{cls.__link}/users/{user_id}/subjects/{subject_name}/?role={role}"
        response = get(url)

        return ApiUtils.create_api_response(response, ItemsDto[PrivateCourseInlineDto])

    @classmethod
    def get_classes(cls, private_course_id: int, role: str, user_id: int, page: int = 1) -> ApiResponse[PaginatedList[PrivateClassDto]]:
        url = f"{cls.__link}/{private_course_id}/classes/?role={role}&page={page}&user_id={user_id}"
        response = get(url)

        return ApiUtils.create_api_response(response, PaginatedList[PrivateClassDto])
