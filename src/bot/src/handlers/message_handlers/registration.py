from telebot.types import Message
from redis import Redis

from src.common.bot import bot
from src.common.redis_configuration import redis_instance as r

from src.bot.src.handlers.shared import Shared
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.user_client import UserClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.validators import Validator
from src.common.storage import Storage


class RegistrationContext:
    @staticmethod
    def start_function(message: Message, redis: Redis, *args, **kwargs):
        chat_id = message.from_user.id

        response = UserClient.get_me(tg_data=message)

        if response.is_successful():
            user = response.data
            Storage().add_user(chat_id, user)

            markup = InlineKeyboardMarkupCreator.main_menu_markup(chat_id, user.locale)
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "Welcome", user.locale, name=user.first_name),
                             reply_markup=markup)
            return

        redis.hset(str(chat_id), "id", int(chat_id))

        welcome_message = """
        Hi, it's TutorillaBot!\nMy mission is to help you to find a tutor for your needs.\n\nPlease, select a language by clicking the button below to start the registration process.
        """

        bot.send_message(chat_id=chat_id, text=welcome_message,
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
