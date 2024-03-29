from telebot.types import CallbackQuery
from bot.bot_token import bot
from bot.handlers.shared import role_requests
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.admin_client import AdminClient
from bot.api.api_models import UserRequestDto, UserDto
from bot.enums import Role
from bot.redis.redis_client import r
from bot.exception_handler import log_exception
from typing import Any, List


class AdminActions:
    @staticmethod
    def open_user_request(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role_request_id = callback_data[0]

            request = AdminClient.role_request(role_request_id)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
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
            log_exception(chat_id, AdminActions.open_user_request, e)

    @staticmethod
    def accept_user_request(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            user_id, role = callback_data

            request = AdminClient.accept_user_request(user_id=user_id, role=role)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
                return

            user: UserDto = UserDto(**request.json())

            r.hset(chat_id, "is_student", int(user.is_student))
            r.hset(chat_id, "is_tutor", int(user.is_tutor))
            r.hset(chat_id, "is_admin", int(user.is_admin))

            bot.send_message(chat_id=chat_id, text="User request accepted", disable_notification=True)

        except Exception as e:
            log_exception(chat_id, AdminActions.accept_user_request, e)

    @staticmethod
    def decline_user_request(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            user_id: int = callback_data[0]

            request = AdminClient.decline_user_request(user_id)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
                return

            bot.send_message(chat_id=chat_id, text="User request declined", disable_notification=True)

        except Exception as e:
            log_exception(chat_id, AdminActions.decline_user_request, e)

    @staticmethod
    def back_to_requests(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role: str = callback_data[0]

            role_requests(user_id=chat_id, role=role)

        except Exception as e:
            log_exception(chat_id, AdminActions.back_to_requests, e)
