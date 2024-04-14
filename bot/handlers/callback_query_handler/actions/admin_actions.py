from telebot.types import CallbackQuery
from bot.bot_token import bot
from bot.handlers.shared import role_requests
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.admin_client import AdminClient
from bot.api.api_models import UserRequestDto, UserDto
from bot.enums import Role
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.redis.redis_client import r
from bot.exception_handler import log_exception
from typing import Any, List


class AdminActions:
    @classmethod
    def open_user_request(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role_request_id = callback_data[0]

            request = AdminClient.role_request(role_request_id)

            if not request.ok:
                log_exception(chat_id, cls.open_user_request, api_error=True)
                return

            role_request: UserRequestDto = UserRequestDto(**request.json())

            role: Role | None = None

            if role_request.tutor_role:
                role = Role.Tutor
            elif role_request.student_role:
                role = Role.Student

            markup = InlineKeyboardMarkupCreator.request_decision_markup(user_id=role_request.user.id, role=role)
            bot.send_message(chat_id=chat_id,
                             text=f"Role\n{role_request.user.first_name} {role_request.user.last_name}"
                                  f"\n{role_request.user.email}",
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, cls.open_user_request, e)

    @classmethod
    def accept_user_request(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            user_id, role = callback_data

            request = AdminClient.accept_user_request(user_id=user_id, role=role)

            if not request.ok:
                log_exception(chat_id, cls.accept_user_request, api_error=True)
                return

            user: UserDto = UserDto(**request.json())

            r.hset(user.id, "is_active", int(user.is_active))
            r.hset(user.id, "is_tutor" if user.is_tutor else "is_student", 1)

            cls.__send_confirmation_message(user=user, role=role)

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
            bot.send_message(chat_id=chat_id, text="User's request accepted", disable_notification=True)

        except Exception as e:
            log_exception(chat_id, cls.accept_user_request, e)

    @classmethod
    def decline_user_request(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            user_id: int = callback_data[0]

            request = AdminClient.decline_user_request(user_id)

            if not request.ok:
                log_exception(chat_id, cls.decline_user_request, api_error=True)
                return

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
            bot.send_message(chat_id=chat_id, text="User request declined", disable_notification=True)

        except Exception as e:
            log_exception(chat_id, cls.decline_user_request, e)

    @classmethod
    def back_to_requests(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role: str = callback_data[0]

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
            role_requests(user_id=chat_id, role=role)

        except Exception as e:
            log_exception(chat_id, cls.back_to_requests, e)

    @classmethod
    def __send_confirmation_message(cls, user: UserDto, role: str):
        markup = ReplyKeyboardMarkupCreator.main_menu_markup(user.id)
        bot.send_message(chat_id=user.id, text=f"Congratulations {user.first_name}, Your request for {role} role has been accepted", reply_markup=markup, disable_notification=True)
