from telebot import types
import types as tp


# TODO - remake after better times
def language_callback_checker(func: tp.FunctionType):
    def wrapper(callback: types.CallbackQuery):
        # language = r.hget(str(callback.from_user.id), "language")
        language = "en"

        if language is None:
            user_default_session: dict = {"user_id": callback.from_user.id, "language": "en"}
            # r.hset(str(callback.from_user.id), mapping=user_default_session)
            return func(callback, "en")

        return func(callback, language)

    return wrapper


def language_message_checker(func: tp.FunctionType):
    def wrapper(message: types.Message):
        # language = r.hget(str(message.from_user.id), "language")
        language = "en"

        if language is None:
            # user_default_session: dict = {"user_id": message.from_user.id, "language": "en"}
            # r.hset(str(message.from_user.id), mapping=user_default_session)
            return func(message, "en-US")

        return func(message, language)

    return wrapper
