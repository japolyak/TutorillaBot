from typing import Any
from requests import get, post

from src.core.config import api_link
from src.core.models import ItemsDto, TutorCourseInlineDto, BlaTutorCourseDto
from ..http_client import HTTPClient, ApiResponse

from src.bot.src.services.api.api_utils import ApiUtils


class TutorCourseClient:
    client = HTTPClient("tutor-courses")
    __link = f"{api_link}/tutor-courses"

    @classmethod
    def course_tutors(cls, subject_name: str, **kwargs) -> ApiResponse[ItemsDto[TutorCourseInlineDto]]:
        url = f"subject-name/{subject_name}/"

        return cls.client.check_session(**kwargs).get(url, ItemsDto[TutorCourseInlineDto])

    @classmethod
    def enroll_in_course(cls, tutor_course_id: int, **kwargs) -> ApiResponse[Any]:
        url = f"{tutor_course_id}/"

        return cls.client.check_session(**kwargs).post(url, None)

    @classmethod
    def add_course(cls, user_id: int, payload):
        url = f"{cls.__link}/users/{user_id}/"
        response = post(url, data=payload)

        return response

    @classmethod
    def get_courses(cls, user_id) -> ApiResponse[ItemsDto[BlaTutorCourseDto]]:
        url = f"{cls.__link}/users/{user_id}/"
        response = get(url)

        return ApiUtils.create_api_response(response, ItemsDto[BlaTutorCourseDto])
