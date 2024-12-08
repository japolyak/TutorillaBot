from hashlib import sha256
from hmac import new as hmac_new
from urllib.parse import unquote, quote
import time
import json
from typing import Union, Optional
from telebot.types import CallbackQuery, Message

from src.common.config import bot_token
from src.common.models import BaseDto
from src.common.string_utils import StringUtils


class TelegramUser(BaseDto):
    id: int
    first_name: str
    last_name: str


class TelegramInitData:
    # Implementation based on https://gist.github.com/nukdokplex/79438159cb4e757c15ded719e1a83163
    __dict_value: Optional[dict] = None
    __hash_string = ""
    from_bot: bool = False
    user: Optional[TelegramUser] = None

    def __init__(self, init_data: Optional[str] = None):
        if StringUtils.is_none_or_empty(init_data):
            return

        self.__dict_value = dict()

        for chunk in init_data.split("&"):
            [key, value] = chunk.split("=", 1)
            if key == "hash":
                self.__hash_string = value
                continue

            if key == 'from_bot':
                self.from_bot = True
                continue

            self.__dict_value[key] = unquote(value)

        user_data = json.loads(self.__dict_value['user'])

        self.user = TelegramUser.model_validate(user_data)

    def is_valid(self) -> bool:
        if StringUtils.is_none_or_empty(self.__hash_string):
            return False

        computed_hash = self.__create_hash(self.__dict_value)

        return computed_hash == self.__hash_string

    def create_str_init_data(self, tg_data: Union[Message, CallbackQuery], params: Optional[dict]) -> str:
        user = tg_data.from_user

        init_data_dict = dict()

        if type(tg_data) == Message:
            init_data_dict['message_id'] = f'{tg_data.message_id}'
        elif type(tg_data) == CallbackQuery:
            init_data_dict['inline_message_id'] = f'{tg_data.inline_message_id}'

        init_data_dict['user'] = f'{{"id":{user.id},"first_name":"{user.first_name}","last_name":"{user.last_name}","language_code":"{user.language_code}"}}'
        init_data_dict['auth_date'] = f'{int(time.time())}'

        init_data = "&".join(f"{key}={quote(str(value))}" for key, value in init_data_dict.items())

        computed_hash = self.__create_hash(init_data_dict)
        init_data += f"&hash={computed_hash}"

        if params:
            init_data += "&" + "&".join(f"{key}={quote(str(value))}" for key, value in params.items())

        return init_data

    @staticmethod
    def __create_hash(init_data_dict: dict, c_str="WebAppData") -> str:
        init_data = "\n".join(
            [
                f"{key}={init_data_dict[key]}"
                for key in sorted(init_data_dict.keys())
            ]
        )

        secret_key = hmac_new(c_str.encode(), bot_token.encode(), sha256).digest()
        computed_hash = hmac_new(secret_key, init_data.encode(), sha256).hexdigest()

        return computed_hash
