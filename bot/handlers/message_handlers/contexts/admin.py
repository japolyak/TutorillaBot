from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.handlers.shared import role_requests
from bot.decorators.message_decorator import MessageDecorator


class Admin:
    @staticmethod
    def show_admin_panel(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.admin_guard(chat_id):
                return

            markup = ReplyKeyboardMarkupCreator.admin_panel_markup()
            bot.send_message(chat_id=message.from_user.id,
                             text="Admin panel is here",
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Admin.show_admin_panel, e)

    @staticmethod
    def get_tutor_role_requests(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.admin_guard(chat_id):
                return

            role_requests(user_id=chat_id, role="tutor")

        except Exception as e:
            log_exception(chat_id, Admin.get_tutor_role_requests, e)

    @staticmethod
    def get_student_role_requests(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.admin_guard(chat_id):
                return

            role_requests(user_id=chat_id, role="student")

        except Exception as e:
            log_exception(chat_id, Admin.get_student_role_requests, e)
