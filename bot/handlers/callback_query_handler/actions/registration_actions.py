from telebot.types import ReplyKeyboardRemove, CallbackQuery
from typing import List, Any
from bot.bot_token import bot
from bot.redis.redis_client import r
from bot.i18n.i18n import t
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.registration_client import RegistrationClient
from bot.enums import Role
from bot.handlers.callback_query_handler.callback_prefix import CallBackPrefix
import json
from requests import Response
from bot.exception_handler import log_exception
from bot.handlers.shared import next_stepper
from bot.handlers.message_handlers.registration import registration_first_name


class RegistrationActions:
    @staticmethod
    def registration_locale(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            locale = callback_data[0]

            r.hset(str(chat_id), "locale", locale)

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

            next_stepper(chat_id, t(chat_id, 'ProvideYourFirstname', locale), registration_first_name,
                         ReplyKeyboardRemove(), locale=locale, field="first_name")

        except Exception as e:
            log_exception(chat_id, RegistrationActions.registration_locale, e)

    @staticmethod
    def registration_time_zone(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            timezone, locale = callback_data

            r.hset(str(chat_id), "time_zone", timezone)

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

            payload = json.dumps(r.hgetall(str(chat_id)), indent=4)

            request = RegistrationClient.signup_user(payload)

            if not request.ok:
                fields_to_pop = ["last_name", "first_name", "email", "time_zone", "locale"]

                [r.hdel(chat_id, x) for x in fields_to_pop]

                log_exception(chat_id, RegistrationActions.registration_time_zone)
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
            log_exception(chat_id, RegistrationActions.registration_time_zone, e)

    @staticmethod
    def select_role(call: CallbackQuery, *args, **kwargs):
        chat_id = call.from_user.id

        try:
            request: Response | None = None

            if call.data == CallBackPrefix.BecomeTutor:
                request = RegistrationClient.apply_for_role(chat_id, Role.Tutor)
            elif call.data == CallBackPrefix.BecomeStudent:
                request = RegistrationClient.apply_for_role(chat_id, Role.Student)

            if not request.ok:
                log_exception(chat_id, RegistrationActions.select_role)

                return

            r.hset(str(chat_id), "is_active", 0)

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

            bot.send_message(chat_id=chat_id,
                             text=t(call.from_user.id, "GreatWaitForConfirmationByAdmin"),
                             disable_notification=True)

        except Exception as e:
            log_exception(chat_id, RegistrationActions.select_role, e)
