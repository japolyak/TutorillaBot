from redis import Redis
from telebot.types import Message

from src.common.bot import bot
from src.common.models import Role

from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.handlers.shared import Shared
from src.bot.src.services.i18n.i18n import t


class StudentContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis, *args, **kwargs):
            user_id = message.from_user.id
            is_student = redis.hget(user_id, "is_student")

            if is_student == "1":
                return func(user_id, redis)

        return wrapper

    @staticmethod
    @__guard
    def open_classroom(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        markup = ReplyKeyboardMarkupCreator.student_classroom_markup(user_id, locale)

        bot.send_message(chat_id=user_id,
                         text=t(user_id, "YourClassroomIsHere", locale),
                         reply_markup=markup)

    @staticmethod
    @__guard
    def student_courses(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        Shared.get_subjects(user_id, locale, Role.Student, "Courses")

    @staticmethod
    @__guard
    def subscribe_course(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        Shared.send_available_subjects(user_id, locale)
