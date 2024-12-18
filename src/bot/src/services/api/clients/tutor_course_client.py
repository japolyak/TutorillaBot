import requests

from src.core.config import api_link
from src.core.models import ItemsDto, TutorCourseInlineDto, BlaTutorCourseDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class TutorCourseClient:
    __link = f"{api_link}/tutor-courses"

    @classmethod
    def add_course(cls, user_id: int, payload):
        url = f"{cls.__link}/users/{user_id}/"
        response = requests.post(url, data=payload)

        return response

    @classmethod
    def course_tutors(cls, user_id: int, subject_name: str) -> ApiResponse[ItemsDto[TutorCourseInlineDto]]:
        url = f"{cls.__link}/users/{user_id}/subject-name/{subject_name}/"
        response = requests.get(url)

        return ApiUtils.create_api_response(response, ItemsDto[TutorCourseInlineDto])

    @classmethod
    def get_courses(cls, user_id) -> ApiResponse[ItemsDto[BlaTutorCourseDto]]:
        url = f"{cls.__link}/users/{user_id}/"
        response = requests.get(url)

        return ApiUtils.create_api_response(response, ItemsDto[BlaTutorCourseDto])
