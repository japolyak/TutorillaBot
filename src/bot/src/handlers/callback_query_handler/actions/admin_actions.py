from typing import Any, List
from redis import Redis
from telebot.types import CallbackQuery

from src.common.bot import bot
from src.common.models import UserDto

from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.admin_client import AdminClient
from src.bot.src.services.i18n.i18n import t


class AdminActions:
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
    def __send_confirmation_message(cls, user: UserDto, role: str, locale: str):

        markup = ReplyKeyboardMarkupCreator.main_menu_markup(user.id, locale)
        bot.send_message(chat_id=user.id,
                         text=t(user.id, "CongratulationsYourRequestForRoleHasBeenAccepted", locale, name=user.first_name, role=role),
                         reply_markup=markup)
