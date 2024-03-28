from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from typing import Callable
from bot.bot_token import bot
from bot.redis.redis_client import r
from bot.i18n.i18n import t
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.clients.registration_client import RegistrationClient
from bot.enums import CallBackPrefix, Role
from bot.validators import Validator
from bot.api.api_models import UserDto
from bot.redis.redis_user_management import add_user
import json
from requests import Response
from bot.exception_handler import log_exception
from bot.callback_query_agent import get_callback_query_data


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    chat_id = message.from_user.id

    try:
        request = RegistrationClient.get_user(chat_id)

        if request.ok:
            user: UserDto = UserDto(**request.json())

            add_user(chat_id, user)

            markup = ReplyKeyboardMarkupCreator.main_menu_markup(chat_id)
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "Welcome", user.locale, name=user.first_name),
                             disable_notification=True,
                             reply_markup=markup)
            return

        r.hset(str(chat_id), "id", int(chat_id))

        bot.send_message(chat_id=chat_id, text="Select language", reply_markup=InlineKeyboardMarkupCreator.locale_markup())

    except Exception as e:
        log_exception(chat_id, "welcome", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.SetUserLocale))
def registration_locale(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        locale = get_callback_query_data(CallBackPrefix.SetUserLocale, call)[0]

        r.hset(str(chat_id), "locale", locale)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

        next_stepper(chat_id, locale, t(chat_id, 'ProvideYourFirstname', locale), registration_first_name, "first_name",
                     ReplyKeyboardRemove())

    except Exception as e:
        log_exception(chat_id, "registration_locale", e)


def registration_first_name(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.validate_name(message.text):
            next_stepper(chat_id, locale, t(chat_id, "UseOnlyLatinLetters", locale), registration_first_name, field)

            return

        next_registration_step(chat_id, registration_last_name, field, "last_name", message.text, locale, t(message.from_user.id, "ProvideYourLastname"))

    except Exception as e:
        log_exception(chat_id, "registration_first_name", e)


def registration_last_name(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.validate_name(message.text):
            next_stepper(chat_id, locale, t(chat_id, "UseOnlyLatinLetters", locale), registration_last_name, field)

            return

        next_registration_step(chat_id, registration_email, field,
                               "email", message.text, locale, t(chat_id, "ProvideYourEmail", locale))

    except Exception as e:
        log_exception(chat_id, "registration_last_name", e)


def registration_email(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.email_validator(message.text):
            next_stepper(chat_id, locale, t(chat_id, "OneMoreTime", locale), registration_email, field)

            return

        r.hset(str(chat_id), "email", message.text)

        bot.send_message(chat_id=chat_id, text=t(chat_id, "SelectYourTimezone", locale), reply_markup=InlineKeyboardMarkupCreator.timezone_markup(locale))

    except Exception as e:
        log_exception(chat_id, "registration_email", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.SetTimeZone))
def registration_time_zone(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        timezone, locale = get_callback_query_data(CallBackPrefix.SetTimeZone, call)

        r.hset(str(chat_id), "time_zone", timezone)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

        payload = json.dumps(r.hgetall(str(chat_id)), indent=4)
        print(payload)

        request = RegistrationClient.signup_user(payload)

        if not request.ok:
            fields_to_pop = ["last_name", "first_name", "email", "time_zone", "locale"]

            [r.hdel(chat_id, x) for x in fields_to_pop]

            log_exception(chat_id, "registration_time_zone")
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "SomethingWentWrong", locale),
                             disable_notification=True)

            return

        markup = InlineKeyboardMarkupCreator.choose_occupation()
        bot.send_message(chat_id=chat_id,
                         text=t(chat_id, "WelcomeOnBoard", locale),
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, "registration_time_zone", e)


@bot.callback_query_handler(func=lambda call: (call.data in (CallBackPrefix.BecomeTutor, CallBackPrefix.BecomeStudent)))
def select_role(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        request: Response | None = None

        if call.data == CallBackPrefix.BecomeTutor:
            request = RegistrationClient.apply_for_role(chat_id, Role.Tutor)
        elif call.data == CallBackPrefix.BecomeStudent:
            request = RegistrationClient.apply_for_role(chat_id, Role.Student)

        if not request.ok:
            log_exception(chat_id, "select_role API request")

            return

        bot.send_message(chat_id=chat_id,
                         text=t(call.from_user.id, "GreatWaitForConfirmationByAdmin"),
                         disable_notification=True)

    except Exception as e:
        log_exception(chat_id, "select_role", e)
    finally:
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)


def next_stepper(chat_id: int, locale: str, text: str, func: Callable, field=None, markup=None) -> None:
    """
    Sends message and tracks it`s answer

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param locale: Users locale.
    :type locale: :obj:`str`

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
    bot.register_next_step_handler(message=msg, callback=func, field=field, locale=locale)


def next_registration_step(chat_id: int, func: Callable, field: str, next_field: str, data: str, locale: str, msg_text: str, markup=None) -> None:
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

    :param locale: Users locale.
    :type locale: :obj:`str`

    :param msg_text: The text of the message.
    :type msg_text: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """
    r.hset(str(chat_id), field, data)

    next_stepper(chat_id, locale, msg_text, func, next_field, markup)
