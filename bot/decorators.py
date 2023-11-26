from telebot import types
import types as tp
from .api.sessions import SessionApi
from .temporary_session_store import session_store


# Change after Redis will be implemented
def session_checker(func: tp.FunctionType):
    def wrapper(message: types.Message):
        session = session_store.get_session(message.from_user.id)

        if session:
            return func(message)

        data = SessionApi.get_session(message.from_user.id)
        session_store.set_session(message.from_user.id, data)

    return wrapper
