from telebot.types import Message
from src.bot_token import bot
from src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.i18n.i18n import t
from src.redis_service.redis_client import r
from src.handlers.message_handlers.contexts.i_context_base import IContextBase


class MainViewContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message):
            is_active_state = r.hget(message.from_user.id, "is_active")
            if is_active_state == "1" or is_active_state == "0":
                return func(message.from_user.id)

        return wrapper

    @staticmethod
    @__guard
    def main_menu(chat_id: int):
        locale = r.hget(chat_id, "locale")
        markup = ReplyKeyboardMarkupCreator.main_menu_markup(chat_id, locale)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "MainMenu", locale),
                         disable_notification=True, reply_markup=markup)
