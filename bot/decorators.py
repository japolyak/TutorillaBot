from telebot import types
import types as tp
from .redis_client import r


def language_callback_checker(func: tp.FunctionType):
    def wrapper(callback: types.CallbackQuery):
        language = r.hget(str(callback.from_user.id), "language")

        if language is None:
            user_default_session: dict = {"user_id": callback.from_user.id, "language": "en"}
            r.hset(str(callback.from_user.id), mapping=user_default_session)
            return func(callback, "en")

        return func(callback, language)

    return wrapper


def language_message_checker(func: tp.FunctionType):
    def wrapper(message: types.Message):
        language = r.hget(str(message.from_user.id), "language")

        if language is None:
            user_default_session: dict = {"user_id": message.from_user.id, "language": "en"}
            r.hset(str(message.from_user.id), mapping=user_default_session)
            return func(message, "en")

        return func(message, language)

    return wrapper
