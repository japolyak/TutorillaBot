from telebot.types import Message, ReplyKeyboardRemove
from redis import Redis

from src.core.bot.bot import bot
from src.core.redis_configuration import redis_instance as r
from src.core.storage import Storage

from src.bot.src.handlers.shared import Shared
from src.core.bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.user_client import UserClient
from src.bot.src.validators import Validator
from src.core.i18n.i18n import t
from src.core.bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator


class RegistrationContext:
    @staticmethod
    def start_function(message: Message, redis: Redis, *args, **kwargs):
        chat_id = message.from_user.id

        response = UserClient.get_me(tg_data=message)

        if response.is_successful():
            user = response.data
            Storage().add_user(user)

            markup = ReplyKeyboardMarkupCreator.welcome_markup(chat_id, user.locale, is_tutor=user.is_tutor, is_student=user.is_student, is_admin=user.is_admin)
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "Welcome", user.locale, name=user.first_name),
                             reply_markup=markup)
            return

        redis.hset(str(chat_id), "id", int(chat_id))

        bot.send_message(chat_id=chat_id, text=t(chat_id, "WelcomeWord"),
                         reply_markup=ReplyKeyboardRemove())

        bot.send_message(chat_id=chat_id, text=t(chat_id, "SelectLanguage"),
                         reply_markup=InlineKeyboardMarkupCreator.locale_markup())


def registration_first_name(message: Message, **kwargs):
    chat_id = message.from_user.id
    field = kwargs.get("field")
    locale = kwargs.get("locale")

    if message.content_type != "text" or not Validator.validate_name(message.text):
        Shared.next_stepper(chat_id, t(chat_id, "UseOnlyLatinLetters", locale), registration_first_name,
                     locale=locale, field=field)

        return

    Shared.register_next_step(chat_id, registration_last_name, field, message.text, t(message.from_user.id, "ProvideYourLastname", locale),
                       locale=locale, field="last_name")


def registration_last_name(message: Message, **kwargs):
    chat_id = message.from_user.id
    field = kwargs.get("field")
    locale = kwargs.get("locale")

    if message.content_type != "text" or not Validator.validate_name(message.text):
        Shared.next_stepper(chat_id, t(chat_id, "UseOnlyLatinLetters", locale), registration_last_name, locale=locale, field=field)

        return

    Shared.register_next_step(chat_id, registration_email, field, message.text, t(chat_id, "ProvideYourEmail", locale), locale=locale, field="email")


def registration_email(message: Message, **kwargs):
    chat_id = message.from_user.id
    field = kwargs.get("field")
    locale = kwargs.get("locale")

    if message.content_type != "text" or not Validator.email_validator(message.text):
        Shared.next_stepper(chat_id, t(chat_id, "OneMoreTime", locale), registration_email, locale=locale, field=field)

        return

    r.hset(str(chat_id), "email", message.text)

    bot.send_message(chat_id=chat_id, text=t(chat_id, "SelectYourTimezone", locale),
                     reply_markup=InlineKeyboardMarkupCreator.timezone_markup(locale))
