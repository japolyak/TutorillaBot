from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
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

    next_stepper(message.from_user.id, "First name", registration_first_name, "first_name", ReplyKeyboardRemove())


def registration_first_name(message: Message, field: str):
    if message.content_type != "text" or not Validator.validate_name(message.text):
        next_stepper(message.from_user.id, "Use only latin letters", registration_first_name, field)

        return

    next_registration_step(message.from_user.id, registration_last_name, field, "last_name", message.text, "Last name")


def registration_last_name(message: Message, field: str):
    if message.content_type != "text" or not Validator.validate_name(message.text):
        next_stepper(message.from_user.id, "Use only latin letters", registration_last_name, field)

        return

    next_registration_step(message.from_user.id, registration_email, field, "email", message.text, "Email")


def registration_email(message: Message, field: str):
    if message.content_type != "text" or not Validator.email_validator(message.text):
        next_stepper(message.from_user.id, "One more time", registration_email, field)

        return

    markup = ReplyKeyboardMarkupCreator.choose_time_zone()
    next_registration_step(message.from_user.id, registration_time_zone, field, "time_zone", message.text, "TimeZone", markup)


def registration_time_zone(message: Message, field: str):
    if message.content_type != "text":
        next_stepper(message.from_user.id, "One more time", registration_time_zone, field)

        return

    if not Validator.validate_time_zone(message.text):
        next_stepper(message.from_user.id, "Use only digits", registration_time_zone, field)

        return

    markup = ReplyKeyboardMarkupCreator.phone_markup()
    next_registration_step(message.from_user.id, set_phone, field, "phone_number", message.text, "Phone", markup)


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


def next_stepper(chat_id: int, text: str, func: Callable, field=None, markup=None) -> None:
    """
    Sends message and tracks it`s answer

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param text: The text of the message.
    :type text: :obj:`str`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :field: The field to save in redis.
    :type field: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """

    msg = bot.send_message(chat_id=chat_id, text=text, disable_notification=True, reply_markup=markup)
    bot.register_next_step_handler(message=msg, callback=func, field=field)


def next_registration_step(chat_id: int, func: Callable, field: str, next_field: str, data: str, msg_text: str, markup=None) -> None:
    """
    Saves user`s cache and makes next move

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :field: The field to save in redis.
    :type field: :obj:`str`

    :param next_field: The next field to save in redis.
    :type next_field: :obj:`str`

    :param data: The data to save in redis.
    :type data: :obj:`str`

    :param msg_text: The text of the message.
    :type msg_text: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """
    r.hset(str(chat_id), field, data)

    next_stepper(chat_id, msg_text, func, next_field, markup)


@bot.callback_query_handler(func=lambda call: (call.data in (CallBackPrefix.BecomeTutor, CallBackPrefix.BecomeStudent)))
def become_someone(call: CallbackQuery):
    request = None
    if call.data == CallBackPrefix.BecomeTutor:
        request = RegistrationClient.apply_for_role(call.from_user.id, Role.Tutor)
    elif call.data == CallBackPrefix.BecomeStudent:
        request = RegistrationClient.apply_for_role(call.from_user.id, Role.Student)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id,
                         text="Shit, try later",
                         disable_notification=True)

        return

    bot.send_message(chat_id=call.from_user.id,
                     text="Wait for confirmation by Admin",
                     disable_notification=True)
