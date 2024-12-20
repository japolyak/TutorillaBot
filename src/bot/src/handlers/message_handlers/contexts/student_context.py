from redis import Redis
from telebot.types import Message

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase

from src.core.bot.bot import bot
from src.core.bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.core.i18n.i18n import t
from src.core.models import UserDto


class StudentContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis, *args, **kwargs):
            user = redis.hgetall(message.from_user.id)

            if not user: return

            user = UserDto.model_validate(user)

            if user.is_student or user.is_tutor:
                return func(user)

        return wrapper

    @staticmethod
    @__guard
    def open_classroom(user: UserDto, *args, **kwargs):
        markup = InlineKeyboardMarkupCreator.classroom_markup(user.id, user.locale, is_student=user.is_student, is_tutor=user.is_tutor)

        bot.send_message(chat_id=user.id,
                         text=t(user.id, "YourClassroomIsHere", user.locale),
                         reply_markup=markup)
