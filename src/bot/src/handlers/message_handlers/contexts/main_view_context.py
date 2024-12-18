from redis import Redis
from telebot.types import Message

from src.core.bot.bot import bot

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.i18n.i18n import t


class MainViewContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis, *args, **kwargs):
            user_id = message.from_user.id
            is_active_state = redis.hget(user_id, "is_active")

            if is_active_state == "1" or is_active_state == "0":
                return func(user_id, redis)

        return wrapper

    @staticmethod
    @__guard
    def main_menu(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        markup = InlineKeyboardMarkupCreator.main_menu_markup(user_id, locale)
        bot.send_message(chat_id=user_id, text=t(user_id, "MainMenu", locale), reply_markup=markup)
