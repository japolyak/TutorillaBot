from telebot import types
import types as tp
from .redis_client import r


def session_checker(func: tp.FunctionType):
    def wrapper(message: types.Message):
        language = r.hget(f"{message.from_user.id}", "language")

        if language is None:
            user_default_session: dict = {"user_id": message.from_user.id, "language": "en"}
            r.hset(f"{message.from_user.id}", mapping=user_default_session)
            return func(message, "en")

        return func(message, language)

    return wrapper
