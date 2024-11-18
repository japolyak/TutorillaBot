import requests
from typing import Optional, Union
from telebot.types import Message, CallbackQuery

from src.common.config import api_link
from src.common.telegram_valdiator import TelegramInitData
from src.bot.src.services.redis_service.redis_user_management import RedisManagement

class HTTPClient:
    __base_url = api_link
    token: Optional[str] = None

    def __init__(self, url: str):
        self.module_url = f"{self.__base_url}/{url}/"
        self.session = requests.Session()

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
            url=self.__base_url + "/auth/me/",
            headers=headers
        )

        return response.json()['token']

    def request(self, method, url, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.token}",
            **kwargs,
        }

        response = self.session.request(
            method=method,
            url=self.module_url + url,
            headers=headers
        )

        return response

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)
