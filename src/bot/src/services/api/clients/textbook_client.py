import requests
from typing import Any

from common import api_link, api_timeout
from src.common.models import ItemsDto, TextbookDto

from src.bot.src.services.api.api_utils import ApiUtils, ApiResponse


class TextbookClient:
    __link = f"{api_link}/textbooks"

    @classmethod
    def get_textbooks(cls, tutor_course_id: int) -> ApiResponse[ItemsDto[TextbookDto]]:
        url = f"{cls.__link}/tutor-course/{tutor_course_id}/"
        response = requests.get(url, timeout=api_timeout)

        return ApiUtils.create_api_response(response, ItemsDto[TextbookDto])

    @classmethod
    def save_textbooks(cls, tutor_course_id: int, payload: ItemsDto[str]) -> ApiResponse[None]:
        url = f"{cls.__link}/tutor-course/{tutor_course_id}/"
        response = requests.post(url, data=payload.model_dump_json(), timeout=api_timeout)

        return ApiUtils.create_api_response(response, None)
