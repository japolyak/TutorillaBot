from telebot.types import Message, ReplyKeyboardRemove
from typing import Callable
from ..bot_token import bot
from ..redis_client import r
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.clients.registration_client import RegistrationClient
from ..enums import CallBackPrefix, Role
from ..validators import Validator
from ..api.api_models import UserDto
import json


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    request = RegistrationClient.get_user(message.from_user.id)

    if request.ok:
        user: UserDto = UserDto(**request.json())
        # TODO - add full redis save
        r.hset(message.from_user.id, "is_student", int(user.is_student))
        r.hset(message.from_user.id, "is_tutor", int(user.is_tutor))
        r.hset(message.from_user.id, "is_admin", int(user.is_admin))

        markup = ReplyKeyboardMarkupCreator.main_menu_markup(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text=f"Hi, {user.first_name} {user.last_name}",
                         disable_notification=True,
                         reply_markup=markup)
        return

    r.hset(str(message.from_user.id), "id", message.from_user.id)

    next_stepper(message.from_user.id, "First name", registration_first_name, "first_name")


def registration_first_name(message: Message, field: str):
    if message.content_type != "text" or not Validator.validate_name(message.text):
        next_stepper(message.from_user.id, "Use only latin letters", registration_first_name, field)

        return

    next_registration_step(message, registration_last_name, field, "last_name", "Last name")


def registration_last_name(message: Message, field: str):
    if message.content_type != "text" or not Validator.validate_name(message.text):
        next_stepper(message.from_user.id, "Use only latin letters", registration_last_name, field)

        return

    next_registration_step(message, registration_email, field, "email", "Email")


def registration_email(message: Message, field: str):
    if message.content_type != "text" or not Validator.email_validator(message.text):
        next_stepper(message.from_user.id, "One more time", registration_email, field)

        return

    next_registration_step(message, registration_time_zone, field, "time_zone", "TimeZone")


def registration_time_zone(message: Message, field: str):
    if message.content_type != "text":
        next_stepper(message.from_user.id, "One more time", registration_time_zone, field)

        return

    markup = ReplyKeyboardMarkupCreator.phone_markup()
    next_registration_step(message, set_phone, field, "phone_number", "Phone", markup)


def set_phone(message: Message, field: str):
    if message.content_type != "contact":
        markup = ReplyKeyboardMarkupCreator.phone_markup()

        next_stepper(message.from_user.id, "One more time", set_phone, field, markup)

        return

    phone_number = message.contact.phone_number.replace("+", "")

    r.hset(str(message.from_user.id), field, phone_number)

    bot.send_message(chat_id=message.from_user.id,
                     text="Phone number added",
                     disable_notification=True,
                     reply_markup=ReplyKeyboardRemove())

    payload = json.dumps(r.hgetall(str(message.from_user.id)), indent=4)

    request = RegistrationClient.signup_user(payload)

    if not request.ok:
        fields_to_pop = ["last_name", "first_name", "phone", "email", "time_zone"]
        for x in fields_to_pop:
            r.hdel(message.from_user.id, x)

        bot.send_message(chat_id=message.from_user.id,
                         text="Pizda naturalna. Do it again! Press /start",
                         disable_notification=True)

        return

    markup = InlineKeyboardMarkupCreator.choose_occupation()
    bot.send_message(chat_id=message.from_user.id,
                     text="Congratulations, You have registered and now choose what do You want to do!",
                     disable_notification=True,
                     reply_markup=markup)


def next_stepper(chat_id: int, text: str, func: Callable, field=None, markup=None):
    """
    Sends message and tracks it`s answer
    """

    msg = bot.send_message(chat_id=chat_id, text=text, disable_notification=True, reply_markup=markup)

    bot.register_next_step_handler(message=msg, callback=func, field=field)


def next_registration_step(message: Message, func: Callable, field: str, next_field: str, msg_text: str, markup=None):
    """
    Saves user`s cache and make next move
    """
    r.hset(str(message.from_user.id), field, message.text)

    next_stepper(message.from_user.id, msg_text, func, next_field, markup)


@bot.callback_query_handler(func=lambda call: (call.data in (CallBackPrefix.BecomeTutor, CallBackPrefix.BecomeStudent)))
def become_someone(message: Message):
    request = None
    if message.data == CallBackPrefix.BecomeTutor:
        request = RegistrationClient.apply_for_role(message.from_user.id, Role.Tutor)
    elif message.data == CallBackPrefix.BecomeStudent:
        request = RegistrationClient.apply_for_role(message.from_user.id, Role.Student)

    if not request.ok:
        bot.send_message(chat_id=message.from_user.id,
                         text="Shit, try later",
                         disable_notification=True)

        return

    bot.send_message(chat_id=message.from_user.id,
                     text="Wait for confirmation by Admin",
                     disable_notification=True)
