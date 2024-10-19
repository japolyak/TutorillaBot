from typing import Any, List
from redis import Redis
from telebot.types import CallbackQuery

from common import bot
from src.common.models import UserDto

from src.bot.src.handlers.shared import Shared
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.admin_client import AdminClient
from src.bot.src.services.i18n.i18n import t


class AdminActions:
    @classmethod
    def open_user_request(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        role_request_id, locale = callback_data

        response = AdminClient.role_request(role_request_id)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)

        role_request = response.data

        markup = InlineKeyboardMarkupCreator.request_decision_markup(role_request.user_id, role_request.user_role, locale)
        bot.send_message(chat_id=chat_id,
                         text=f"Role - {role_request.user_role}"
                              f"\n{role_request.user_first_name} {role_request.user_last_name}"
                              f"\n{role_request.user_email}",
                         reply_markup=markup)


    @classmethod
    def accept_user_request(cls, call: CallbackQuery, callback_data: List[Any], redis: Redis, *args, **kwargs):
        chat_id = call.from_user.id

        user_id, role, locale = callback_data

        response = AdminClient.accept_user_request(user_id=user_id, role=role)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        user = response.data

        redis.hset(user.id, "is_active", int(user.is_active))
        redis.hset(user.id, "is_tutor" if user.is_tutor else "is_student", 1)

        cls.__send_confirmation_message(user, role, locale)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "UsersRequestAccepted", locale))


    @classmethod
    def decline_user_request(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        user_id, locale = callback_data

        response = AdminClient.decline_user_request(user_id)

        if not response.ok:
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "UsersRequestDeclined", locale))


    @classmethod
    def back_to_requests(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        role, locale = callback_data

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
        Shared.role_requests(chat_id, role, locale)


    @classmethod
    def __send_confirmation_message(cls, user: UserDto, role: str, locale: str):

        markup = ReplyKeyboardMarkupCreator.main_menu_markup(user.id, locale)
        bot.send_message(chat_id=user.id,
                         text=t(user.id, "CongratulationsYourRequestForRoleHasBeenAccepted", locale, name=user.first_name, role=role),
                         reply_markup=markup)
