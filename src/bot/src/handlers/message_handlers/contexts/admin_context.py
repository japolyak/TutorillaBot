from telebot.types import Message

from src.common.bot_token import bot

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.handlers.shared import role_requests
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_client import r


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
        locale = r.hget(chat_id, "locale")
        markup = ReplyKeyboardMarkupCreator.admin_panel_markup(chat_id, locale)
        bot.send_message(chat_id=chat_id,
                         text=t(chat_id, "AdminPanelIsHere", locale),
                         disable_notification=True,
                         reply_markup=markup)

    @staticmethod
    @__guard
    def get_tutor_role_requests(chat_id: int):
        locale = r.hget(chat_id, "locale")
        role_requests(chat_id, "tutor", locale)

    @staticmethod
    @__guard
    def get_student_role_requests(chat_id: int):
        locale = r.hget(chat_id, "locale")
        role_requests(chat_id, "student", locale)
