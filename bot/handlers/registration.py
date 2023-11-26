import requests
from telebot import types
from ..bot_token import bot
from ..i18n.i18n import t
from ..api.sessions import SessionApi
import logging
from ..temporary_session_store import session_store
from ..markups import MarkupCreator


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    markup = MarkupCreator.language_markup("set")

    bot.send_message(chat_id=message.chat.id,
                     text="Hello! Feel free to adjust your language settings with the options provided.",
                     reply_markup=markup)


# Rewrite after redis implementation
@bot.callback_query_handler(func=lambda call: (call.data == "set ua" or
                                               call.data == "set ru" or
                                               call.data == "set pl" or
                                               call.data == "set en"))
def set_language(call: types.CallbackQuery):
    _, language = call.data.split(" ")

    session: dict = {"user_id": call.from_user.id, "lang": language}

    try:
        SessionApi.set_session(session)

        text = t(language, 'language_changed_to')
        session_store.set_session(user_id=call.from_user.id, data=session)
        bot.send_message(chat_id=call.from_user.id, text=text)
    except requests.RequestException as e:
        logging.error(e)
        bot.send_message(chat_id=call.from_user.id, text="Problem occurred")
