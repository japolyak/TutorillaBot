from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.handlers.message_handlers.contexts.i_context_base import IContextBase
from bot.redis.redis_client import r


class MainView(IContextBase):
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
        try:
            markup = ReplyKeyboardMarkupCreator.main_menu_markup(chat_id)
            bot.send_message(chat_id=chat_id, text="Main menu", disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, MainView.main_menu, e)
