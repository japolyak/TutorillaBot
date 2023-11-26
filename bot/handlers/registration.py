from telebot import types
from ..bot_token import bot
from ..i18n.i18n import t
from ..markups import MarkupCreator
from ..redis_client import r


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    markup = MarkupCreator.language_markup("set")

    bot.send_message(chat_id=message.chat.id,
                     text="Hello! Feel free to adjust your language settings with the options provided.",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data == "set ua" or call.data == "set ru" or
                                               call.data == "set pl" or call.data == "set en"))
def set_language(call: types.CallbackQuery):
    user_cache = r.exists(f"{call.from_user.id}")
    action, language = call.data.split(" ")

    if not user_cache:
        user_session: dict = {"user_id": call.from_user.id, "language": language}
        r.hset(f"{call.from_user.id}", mapping=user_session)

    r.hset(f"{call.from_user.id}", "language", language)

    bot.send_message(chat_id=call.from_user.id,
                     text=t(language, "language_changed_to"))
