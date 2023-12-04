from telebot import types
from typing import Callable
from ..decorators import language_callback_checker
from ..i18n.i18n import t
from ..bot_token import bot
from ..redis_client import r
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.clients.registration_client import RegistrationClient
from ..validators import Validator
from ..api.api_models import User


@bot.message_handler(commands=["start"])
def welcome(message: types.Message):
    request = RegistrationClient.get_user(message.from_user.id)

    if request.ok:
        user = User(**request.json())

        r.hset(message.from_user.id, "is_student", int(user.is_student))
        r.hset(message.from_user.id, "is_tutor", int(user.is_tutor))
        r.hset(message.from_user.id, "is_admin", int(user.is_admin))

        markup = ReplyKeyboardMarkupCreator.main_menu_markup(message.from_user.id)
        bot.send_message(chat_id=message.chat.id, text=f"Hi, {user.first_name} {user.last_name}", reply_markup=markup)
        return

    markup = InlineKeyboardMarkupCreator.language_markup("set")

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
        user_session: dict = {"id": call.from_user.id, "language": language}
        r.hset(str(call.from_user.id), mapping=user_session)

    r.hset(str(call.from_user.id), "language", language)

    bot.send_message(chat_id=call.from_user.id,
                     text=t(language, "selected_language"))

    next_stepper(call.from_user.id, "First name", registration_first_name, language, "first_name")


def registration_first_name(message: types.Message, field: str, language: str):
    if message.content_type != "text":
        next_stepper(message.chat.id, "One more time", registration_first_name, language, field)

        return

    next_registration_step(message, registration_last_name, field, "last_name", "Last name", language)


def registration_last_name(message: types.Message, field: str, language: str):
    if message.content_type != "text":
        next_stepper(message.chat.id, "One more time", registration_last_name, language, field)

        return

    next_registration_step(message, registration_email, field, "email", "Email", language)


def registration_email(message: types.Message, field: str, language: str):
    if message.content_type != "text" or not Validator.email_validator(message.text):
        next_stepper(message.chat.id, "One more time", registration_email, language, field)

        return

    markup = ReplyKeyboardMarkupCreator.phone_markup(language)
    next_registration_step(message, set_phone, field, "phone_number", "Phone", language, markup)


def set_phone(message: types.Message, field: str, language: str):
    if message.content_type != "contact":
        markup = ReplyKeyboardMarkupCreator.phone_markup(language)

        next_stepper(message.chat.id, "One more time", set_phone, language, field, markup)

        return

    phone_number = message.contact.phone_number.replace("+", "")

    r.hset(str(message.from_user.id), field, phone_number)

    bot.send_message(chat_id=message.chat.id, text="Phone number added", reply_markup=types.ReplyKeyboardRemove())

    payload = r.hgetall(str(message.from_user.id))
    payload["is_student"] = False
    payload["is_tutor"] = False
    payload["is_admin"] = False
    payload["normalized_email"] = payload["email"].lower()

    request = RegistrationClient.signup_user(payload)

    if not request.ok:
        fields_to_pop = ["last_name", "first_name", "phone", "email"]
        for x in fields_to_pop:
            r.hdel(message.from_user.id, x)

        bot.send_message(chat_id=message.chat.id,
                         text="Pizda naturalna. Do it again! Press /start")

        return

    markup = InlineKeyboardMarkupCreator.choose_occupation()
    bot.send_message(chat_id=message.chat.id,
                     text="Congratulations, You have registered and now choose what do You want to do!",
                     reply_markup=markup)


def next_stepper(chat_id: int, text: str, func: Callable, language: str, field=None, markup=None):
    """
    Sends message and tracks it`s answer
    """
    msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    bot.register_next_step_handler(message=msg, callback=func, field=field, language=language)


def next_registration_step(message: types.Message, func: Callable, field: str, next_field: str, msg_text: str,
                           language: str, markup=None):
    """
    Saves user`s cache and make next move
    """
    r.hset(str(message.from_user.id), field, message.text)

    next_stepper(message.from_user.id, msg_text, func, language, next_field, markup)


@bot.callback_query_handler(func=lambda call: (call.data == "student"))
@language_callback_checker
def become_student(message: types.Message, language: str):
    request = RegistrationClient.apply_for_student_role(message.from_user.id)

    if not request.ok:
        markup = InlineKeyboardMarkupCreator.choose_occupation()
        next_stepper(chat_id=message.from_user.id,
                     text="Shit, not good. Try again later!",
                     func=become_student,
                     language=language,
                     markup=markup)

        return

    r.hset(message.from_user.id, "is_student", 1)
    r.hset(message.from_user.id, "is_tutor", 0)
    r.hset(message.from_user.id, "is_admin", 0)
    markup = ReplyKeyboardMarkupCreator.main_menu_markup(message.from_user.id)
    bot.send_message(chat_id=message.from_user.id,
                     text="Confirmed!",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data == "tutor"))
@language_callback_checker
def become_tutor(message: types.Message, language: str):
    request = RegistrationClient.apply_for_tutor_role(message.from_user.id)

    if not request.ok:
        markup = InlineKeyboardMarkupCreator.choose_occupation()
        next_stepper(chat_id=message.from_user.id,
                     text="Shit, not good. Try again later!",
                     func=become_tutor,
                     language=language,
                     markup=markup)

        return

    r.hset(message.from_user.id, "is_tutor", 1)
    r.hset(message.from_user.id, "is_student", 0)
    r.hset(message.from_user.id, "is_admin", 0)
    markup = ReplyKeyboardMarkupCreator.main_menu_markup(message.from_user.id)
    bot.send_message(chat_id=message.from_user.id,
                     text="Confirmed!",
                     reply_markup=markup)


# region TODO - Delete later
@bot.message_handler(regexp="Restore")
def restore_redis(message: types.Message):
    payload = r.hgetall(str(message.from_user.id))

    new_payload = payload.pop('phone')
    new_payload = payload.pop('language')
    print(payload)
    RegistrationClient.signup_user(payload)

    # bot.send_message(chat_id=message.chat.id, text="Restored", reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(chat_id=message.chat.id, text="Restored")
# endregion
