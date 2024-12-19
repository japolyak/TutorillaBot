from redis import Redis
from telebot.types import Message

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase

from src.core.bot.bot import bot
from src.core.i18n.i18n import t
from src.core.models import UserDto
from src.core.config import support_nick


class UserContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis, *args, **kwargs):
            user = redis.hgetall(message.from_user.id)

            if not user: return

            user = UserDto.model_validate(user)

            if user.is_active:
                return func(user)

        return wrapper

    @staticmethod
    @__guard
    def open_profile(user: UserDto, *args, **kwargs):
        bot.send_message(
            chat_id=user.id,
            text=t(user.id, "ItsYourProfile", user.locale, first_name=user.first_name, last_name=user.last_name)
        )

    @staticmethod
    @__guard
    def support(user: UserDto, *args, **kwargs):
        bot.send_message(chat_id=user.id, text=t(user.id, "ContactSupportAccount", user.locale, support_nick=support_nick))
