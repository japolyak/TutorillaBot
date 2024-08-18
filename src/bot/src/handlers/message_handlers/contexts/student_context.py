from telebot.types import Message

from src.common.bot_token import bot
from src.common.models import Role

from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.handlers.shared import get_subjects
from src.bot.src.handlers.shared import send_available_subjects
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_client import r


class StudentContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message):
            is_student = r.hget(message.from_user.id, "is_student")
            if is_student == "1":
                return func(message.from_user.id)

        return wrapper

    @staticmethod
    @__guard
    def open_classroom(chat_id: int):
        locale = r.hget(chat_id, "locale")
        markup = ReplyKeyboardMarkupCreator.student_classroom_markup(chat_id, locale)

        bot.send_message(chat_id=chat_id,
                         text=t(chat_id, "YourClassroomIsHere", locale),
                         disable_notification=True,
                         reply_markup=markup)

    @staticmethod
    @__guard
    def student_courses(chat_id: int):
        locale = r.hget(chat_id, "locale")
        get_subjects(chat_id, Role.Student, locale)

    @staticmethod
    @__guard
    def subscribe_course(chat_id: int):
        locale = r.hget(chat_id, "locale")
        send_available_subjects(chat_id, locale)
