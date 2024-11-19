from requests import Response, Session
from typing import Optional, Union, Generic, Type, Any
from telebot.types import Message, CallbackQuery

from src.common.models import T, ErrorDto, TokenDto
from src.common.config import api_link
from src.common.telegram_valdiator import TelegramInitData
from src.bot.src.services.redis_service.redis_user_management import RedisManagement


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T] = None, error: Optional[ErrorDto] = None):
        self.__success = data is not None
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        return self.__success


class HTTPClient:
    __base_url = api_link
    token: Optional[str] = None

    def __init__(self, url: str):
        self.module_url = f"{self.__base_url}/{url}/"
        self.session = Session()

    def check_session(self, **kwargs):
        if kwargs["tg_data"] is None:
            raise Exception('No TG data was passed')

        tg_data: Optional[Union[Message, CallbackQuery]] = kwargs["tg_data"]

        token = RedisManagement().get_user_token(tg_data.from_user.id)

        if token is None:
            init_data = TelegramInitData.create(tg_data)
            token = self.__authenticate(init_data)

        if token is None:
            raise Exception('Token was not got:(')

        self.token = token
        RedisManagement().set_user_token(tg_data.from_user.id, token)

        return self

    def __authenticate(self, init_data: str) -> Optional[str]:
        headers = {
            "Init-Data": init_data,
        }

        response = self.session.request(
            method="GET",
            url=self.__base_url + "/auth/tg/",
            headers=headers
        )

        result = self.__response(response, TokenDto)

        if not result.is_successful():
            raise Exception('Token was not got:(')

        return result.data.token

    def request(self, method, url, model_class: Type[T], **kwargs):
        data = kwargs.get("data")
        passed_headers: Optional[dict] = kwargs.get("headers")

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        if passed_headers is not None:
            headers.update(**passed_headers)

        response = self.session.request(
            method=method,
            url=self.module_url + url,
            data=data,
            headers=headers
        )

        return self.__response(response, model_class)

    @classmethod
    def __response(cls, response: Response, model_class: Type[T]) -> ApiResponse[T]:
        if not response.ok:
            error = ErrorDto(**response.json())
            return ApiResponse[T](error=error)

        # TODO - rethink implementation
        if model_class is None and response.ok:
            return ApiResponse[T](data=Any)

        json_data = response.json()
        data = model_class(**json_data)

        return ApiResponse[T](data=data)

    def get(self, url, model_class: Type[T], **kwargs):
        return self.request("GET", url, model_class, **kwargs)

    def post(self, url, model_class: Type[T], **kwargs):
        return self.request("POST", url, model_class, **kwargs)

    def put(self, url, model_class: Type[T], **kwargs):
        return self.request("PUT", url, model_class, **kwargs)

    def delete(self, model_class: Type[T], url, **kwargs):
        return self.request("DELETE", url, model_class, **kwargs)
