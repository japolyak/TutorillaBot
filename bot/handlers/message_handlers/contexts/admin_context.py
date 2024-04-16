from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.handlers.shared import role_requests
from bot.i18n.i18n import t
from bot.redis.redis_client import r
from bot.handlers.message_handlers.contexts.i_context_base import IContextBase


class AdminContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message):
            is_admin = r.hget(message.from_user.id, "is_admin")
            if is_admin == "1":
                return func(message.from_user.id)

        return wrapper

    @staticmethod
    @__guard
    def show_admin_panel(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.admin_panel_markup(chat_id, locale)
            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "AdminPanelIsHere", locale),
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, AdminContext.show_admin_panel, e)

    @staticmethod
    @__guard
    def get_tutor_role_requests(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            role_requests(chat_id, "tutor", locale)

        except Exception as e:
            log_exception(chat_id, AdminContext.get_tutor_role_requests, e)

    @staticmethod
    @__guard
    def get_student_role_requests(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            role_requests(chat_id, "student", locale)

        except Exception as e:
            log_exception(chat_id, AdminContext.get_student_role_requests, e)
