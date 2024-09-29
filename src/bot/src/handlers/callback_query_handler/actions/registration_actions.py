import json
from redis import Redis
from requests import Response
from telebot.types import ReplyKeyboardRemove, CallbackQuery
from typing import List, Any

from common import bot
from src.common.models import Role

from src.bot.src.services.i18n.i18n import t
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.registration_client import RegistrationClient
from src.bot.src.handlers.callback_query_handler.callback_prefix import CallBackPrefix
from src.bot.src.handlers.shared import Shared
from src.bot.src.handlers.message_handlers.registration import registration_first_name


class RegistrationActions:
    @staticmethod
    def registration_locale(call: CallbackQuery, callback_data: List[Any], redis: Redis):
        chat_id = call.from_user.id

        locale = callback_data[0]

        redis.hset(str(chat_id), "locale", locale)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

        Shared.next_stepper(chat_id, t(chat_id, 'ProvideYourFirstname', locale), registration_first_name,
                     ReplyKeyboardRemove(), locale=locale, field="first_name")

    @staticmethod
    def registration_time_zone(call: CallbackQuery, callback_data: List[Any], redis: Redis):
        chat_id = call.from_user.id

        timezone, locale = callback_data

        redis.hset(str(chat_id), "time_zone", timezone)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

        payload = json.dumps(redis.hgetall(str(chat_id)), indent=4)

        response = RegistrationClient.signup_user(payload)

        if not response.ok:
            fields_to_pop = ["last_name", "first_name", "email", "time_zone", "locale"]

            [redis.hdel(chat_id, x) for x in fields_to_pop]

            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "SomethingWentWrong", locale))

            return

        markup = InlineKeyboardMarkupCreator.choose_occupation(chat_id, locale)
        bot.send_message(chat_id=chat_id,
                         text=t(chat_id, "WelcomeOnBoard", locale),
                         reply_markup=markup)

    @staticmethod
    def select_role(call: CallbackQuery, callback_data: List[Any], redis: Redis, **kwargs):
        chat_id = call.from_user.id

        response: Response | None = None

        prefix, locale = call.data.split()

        if prefix == CallBackPrefix.BecomeTutor:
            response = RegistrationClient.apply_for_role(chat_id, Role.Tutor)
        elif prefix == CallBackPrefix.BecomeStudent:
            response = RegistrationClient.apply_for_role(chat_id, Role.Student)

        if not response.ok:
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "RetrievingDataError", locale))

            return

        redis.hset(str(chat_id), "is_active", 0)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

        bot.send_message(chat_id=chat_id,
                         text=t(call.from_user.id, "GreatWaitForConfirmationByAdmin", locale))
