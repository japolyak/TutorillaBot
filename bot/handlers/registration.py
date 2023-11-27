from telebot import types
from ..bot_token import bot
from ..i18n.i18n import t
from ..markups import MarkupCreator
from ..redis_client import r


@bot.message_handler(commands=["start"])
def welcome(message: types.Message):
    markup = MarkupCreator.language_markup("set")

    bot.send_message(chat_id=message.chat.id,
                     text="Hello! Feel free to adjust your language settings with the options provided.",
                     reply_markup=markup)


# TODO - rewrite after change language button will be implemented
@bot.callback_query_handler(func=lambda call: (call.data == "set ua" or call.data == "set ru" or
                                               call.data == "set pl" or call.data == "set en"))
def set_language(call: types.CallbackQuery):
    """
    First language setup
    """
    user_cache = r.exists(f"{call.from_user.id}")
    _, language = call.data.split(" ")

    if not user_cache:
        user_session: dict = {"user_id": call.from_user.id, "language": language}
        r.hset(str(call.from_user.id), mapping=user_session)

    r.hset(str(call.from_user.id), "language", language)

    bot.send_message(chat_id=call.from_user.id,
                     text=t(language, "selected_language"))

    msg = bot.send_message(chat_id=call.from_user.id,
                           text="First name")

    bot.register_next_step_handler(message=msg,
                                   callback=registration_first_name,
                                   field="first_name",
                                   language=language)


def registration_first_name(message: types.Message, field: str, language: str):
    if message.content_type != "text":
        repeat_step(message.chat.id, registration_first_name, field, language)

        return

    next_registration_step(message, registration_last_name, field, "last_name", "Last name", language)


def registration_last_name(message: types.Message, field: str, language: str):
    if message.content_type != "text":
        repeat_step(message.chat.id, registration_last_name, field, language)

        return

    next_registration_step(message, registration_email, field, "email", "Email", language)


def registration_email(message: types.Message, field: str, language: str):
    if message.content_type != "text":
        repeat_step(message.chat.id, registration_email, field, language)

        return

    markup = MarkupCreator.phone_markup(language)
    next_registration_step(message, set_phone, field, "phone", "Phone", language, markup)


def set_phone(message: types.Message, field: str, language: str):
    if message.content_type != "contact":
        markup = MarkupCreator.phone_markup(language)

        repeat_step(message.chat.id, set_phone, field, language, markup)

        return

    phone_number = message.contact.phone_number.replace("+", "")

    r.hset(str(message.from_user.id), field, phone_number)
    # TODO - translation
    bot.send_message(chat_id=message.chat.id, text="Телефон добавлен", reply_markup=types.ReplyKeyboardRemove())
    # TODO - translation
    markup = MarkupCreator.restore_redis_markup()
    # markup = MarkupCreator.choose_occupation(language)
    bot.send_message(chat_id=message.chat.id,
                     text="Congratulations, You have registered and now choose what do You want to do!",
                     reply_markup=markup)


def repeat_step(chat_id, funct, field, language, markup=None):
    msg = bot.send_message(chat_id=chat_id, text="One more time", reply_markup=markup)

    bot.register_next_step_handler(message=msg,
                                   callback=funct,
                                   field=field,
                                   language=language)


def next_registration_step(message, fct,  field, next_field, msg_text, language, markup=None):
    r.hset(str(message.from_user.id), field, message.text)

    msg = bot.send_message(chat_id=message.from_user.id,
                           text=msg_text,
                           reply_markup=markup)

    bot.register_next_step_handler(message=msg,
                                   callback=fct,
                                   field=next_field,
                                   language=language)


# TODO - Delete later
@bot.message_handler(regexp="Restore")
def restore_redis(message: types.Message):
    r.hdel(message.from_user.id, "last_name")
    r.hdel(message.from_user.id, "first_name")
    r.hdel(message.from_user.id, "phone")
    r.hdel(message.from_user.id, "email")

    bot.send_message(chat_id=message.chat.id, text="Restored", reply_markup=types.ReplyKeyboardRemove())
