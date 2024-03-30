from telebot.types import Message
from bot.bot_token import bot
from bot.redis.redis_client import r
from bot.i18n.i18n import t
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.clients.registration_client import RegistrationClient
from bot.validators import Validator
from bot.api.api_models import UserDto
from bot.redis.redis_user_management import add_user
from bot.exception_handler import log_exception
from bot.handlers.shared import next_stepper, next_registration_step


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
        log_exception(chat_id, welcome, e)


def registration_first_name(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.validate_name(message.text):
            next_stepper(chat_id, locale, t(chat_id, "UseOnlyLatinLetters", locale), registration_first_name, field)

            return

        next_registration_step(chat_id, registration_last_name, field, "last_name", message.text, locale, t(message.from_user.id, "ProvideYourLastname"))

    except Exception as e:
        log_exception(chat_id, registration_first_name, e)


def registration_last_name(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.validate_name(message.text):
            next_stepper(chat_id, locale, t(chat_id, "UseOnlyLatinLetters", locale), registration_last_name, field)

            return

        next_registration_step(chat_id, registration_email, field,
                               "email", message.text, locale, t(chat_id, "ProvideYourEmail", locale))

    except Exception as e:
        log_exception(chat_id, registration_last_name, e)


def registration_email(message: Message, field: str, locale: str):
    chat_id = message.from_user.id

    try:
        if message.content_type != "text" or not Validator.email_validator(message.text):
            next_stepper(chat_id, locale, t(chat_id, "OneMoreTime", locale), registration_email, field)

            return

        r.hset(str(chat_id), "email", message.text)

        bot.send_message(chat_id=chat_id, text=t(chat_id, "SelectYourTimezone", locale), reply_markup=InlineKeyboardMarkupCreator.timezone_markup(locale))

    except Exception as e:
        log_exception(chat_id, registration_email, e)