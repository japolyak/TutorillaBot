from hashlib import sha256
from hmac import new as hmac_new
from urllib.parse import unquote, quote
import time
from typing import Union
from telebot.types import CallbackQuery, Message

from src.common.config import bot_token


class TelegramInitData:
    @classmethod
    def validate(cls, init_data: str) -> bool:
        # Reimplemented based on https://gist.github.com/nukdokplex/79438159cb4e757c15ded719e1a83163
        hash_string = ""

        init_data_dict = dict()

        for chunk in init_data.split("&"):
            [key, value] = chunk.split("=", 1)
            if key == "hash":
                hash_string = value
                continue
            init_data_dict[key] = unquote(value)

        if hash_string == "":
            return False

        computed_hash = cls.__create_hash(init_data_dict)

        return computed_hash == hash_string

    @classmethod
    def create(cls, tg_data: Union[Message, CallbackQuery]) -> str:
        user = tg_data.from_user

        init_data_dict = dict()

        if type(tg_data) == Message:
            init_data_dict['message_id'] = tg_data.message_id
        elif type(tg_data) == CallbackQuery:
            init_data_dict['inline_message_id'] = tg_data.inline_message_id

        init_data_dict['user'] = f'{{"id":{user.id},"first_name":"{user.first_name}","last_name":"{user.last_name}","language_code":"{user.language_code}"}}'
        init_data_dict['auth_date'] = int(time.time())

        init_data = "&".join(f"{key}={quote(str(value))}" for key, value in init_data_dict.items())

        computed_hash = cls.__create_hash(init_data_dict)
        init_data += f"&hash={computed_hash}"

        return init_data

    @classmethod
    def __create_hash(cls, init_data_dict: dict, c_str="WebAppData") -> str:
        init_data = "\n".join(
            [
                f"{key}={init_data_dict[key]}"
                for key in sorted(init_data_dict.keys())
            ]
        )

        secret_key = hmac_new(c_str.encode(), bot_token.encode(), sha256).digest()
        computed_hash = hmac_new(secret_key, init_data.encode(), sha256).hexdigest()

        return computed_hash
