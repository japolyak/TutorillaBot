from requests import Response, Session
from requests.cookies import RequestsCookieJar
from typing import Optional, Union, Generic, Type, Any, Tuple
from telebot.types import Message, CallbackQuery

from src.common.config import api_link
from src.common.logger import log
from src.common.models import T, ErrorDto, TokenDto
from src.common.storage import Storage
from src.common.telegram_init_data import TelegramInitData


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T] = None, error: Optional[ErrorDto] = None):
        self.__success = data is not None
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        return self.__success


class HTTPClient:
    _base_url = api_link
    _access_token: Optional[str] = None

    def __init__(self, url: str):
        self.module_url = f"{self._base_url}/{url}/"
        self.session = Session()

    def check_session(self, **kwargs):
        if kwargs["tg_data"] is None: self._log_bad_request('No TG data was passed')

        tg_data: Optional[Union[Message, CallbackQuery]] = kwargs["tg_data"]

        access_token = Storage().get_access_token(tg_data.from_user.id)
        refresh_token_id = Storage().get_refresh_token_id(tg_data.from_user.id)

        if access_token and refresh_token_id: return self._set_current_session(access_token, refresh_token_id)

        if refresh_token_id is None:
            init_data = TelegramInitData().create_str_init_data(tg_data, {"from_bot": True})

            access_token, refresh_token_id = self._authenticate(init_data)
            Storage().set_refresh_token_id(tg_data.from_user.id, refresh_token_id)
        else:
            access_token = self._refresh_access_token(refresh_token_id)

        Storage().set_access_token(tg_data.from_user.id, access_token)

        return self._set_current_session(access_token, refresh_token_id)

    def request(self, method, url, model_class: Type[T], **kwargs):
        data = kwargs.get("data")
        passed_headers: Optional[dict] = kwargs.get("headers")

        headers = {
            "Authorization": f"Bearer {self._access_token}"
        }

        if passed_headers is not None:
            headers.update(**passed_headers)

        response = self.session.request(
            method=method,
            url=self.module_url + url,
            data=data,
            headers=headers
        )

        return self._response(response, model_class)[0]

    def get(self, url, model_class: Type[T], **kwargs):
        return self.request("GET", url, model_class, **kwargs)

    def post(self, url, model_class: Type[T], **kwargs):
        return self.request("POST", url, model_class, **kwargs)

    def put(self, url, model_class: Type[T], **kwargs):
        return self.request("PUT", url, model_class, **kwargs)

    def delete(self, model_class: Type[T], url, **kwargs):
        return self.request("DELETE", url, model_class, **kwargs)

    #region Private methods
    @classmethod
    def _response(cls, response: Response, model_class: Type[T]) ->Tuple[ApiResponse[T], Optional[RequestsCookieJar]]:
        if not response.ok:
            error = ErrorDto(**response.json())
            return ApiResponse[T](error=error), None

        # TODO - rethink implementation
        if model_class is None and response.ok:
            return ApiResponse[T](data=Any), response.cookies

        json_data = response.json()
        data = model_class(**json_data)

        return ApiResponse[T](data=data), response.cookies

    def _set_current_session(self, access_token, refresh_token_id):
        self._access_token = access_token
        self.session.cookies.set("refreshTokenId", refresh_token_id)
        return self

    def _authenticate(self, init_data: str) -> Tuple[str, str]:
        response = self.session.request(
            method="GET",
            url=self._base_url + "/auth/me/",
            headers={
                "Init-Data": init_data,
            }
        )

        result, cookies = self._response(response, TokenDto)

        if not result.is_successful() or result.data is None: self._log_bad_request('No access token')

        session_key = cookies.get("refreshTokenId")

        if not session_key: self._log_bad_request('No refresh token id')

        return result.data.access_token, session_key

    def _refresh_access_token(self, refresh_token_id: str) -> str:
        response = self.session.request(
            method="GET",
            url=self._base_url + "/auth/refresh/",
            cookies={
                'refreshTokenId': refresh_token_id
            }
        )

        result, _ = self._response(response, TokenDto)

        if not result.is_successful(): self._log_bad_request('User is unauthorized')

        if result.data is None: self._log_bad_request('No access token')

        return result.data.access_token

    def _log_bad_request(self, msg: str):
        log.info(msg)
        raise Exception(msg)
    #endregion