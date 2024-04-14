from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.handlers.shared import role_requests
from bot.decorators.message_decorator import MessageDecorator
from bot.i18n.i18n import t
from bot.redis.redis_client import r


class Admin:
    @staticmethod
    def show_admin_panel(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.admin_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.admin_panel_markup(locale)
            bot.send_message(chat_id=message.from_user.id,
                             text=t(chat_id, "AdminPanelIsHere", locale),
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

            locale = r.hget(chat_id, "locale")
            role_requests(chat_id, "tutor", locale)

        except Exception as e:
            log_exception(chat_id, Admin.get_tutor_role_requests, e)

    @staticmethod
    def get_student_role_requests(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.admin_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            role_requests(chat_id, "student", locale)

        except Exception as e:
            log_exception(chat_id, Admin.get_student_role_requests, e)
