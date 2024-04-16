from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.handlers.message_handlers.contexts.i_base import IBase
from bot.redis.redis_client import r


class Student(IBase):
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
        try:
            markup = ReplyKeyboardMarkupCreator.student_classroom_markup()

            bot.send_message(chat_id=chat_id,
                             text="Your classroom is here",
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Student.open_classroom, e)

    @staticmethod
    @__guard
    def student_courses(chat_id: int):
        try:
            get_subjects(chat_id, "student")

        except Exception as e:
            log_exception(chat_id, Student.student_courses, e)

    @staticmethod
    @__guard
    def subscribe_course(chat_id: int):
        try:
            send_available_subjects(user_id=chat_id)

        except Exception as e:
            log_exception(chat_id, Student.subscribe_course, e)
