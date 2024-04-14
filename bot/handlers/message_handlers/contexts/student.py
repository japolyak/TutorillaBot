from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator
from bot.i18n.i18n import t
from bot.redis.redis_client import r


class Student:
    @classmethod
    def open_classroom(cls, message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.student_classroom_markup(locale)

            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "YourClassroomIsHere", locale),
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, cls.open_classroom, e)

    @classmethod
    def student_courses(cls, message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            get_subjects(chat_id, "student", locale)

        except Exception as e:
            log_exception(chat_id, cls.student_courses, e)

    @classmethod
    def subscribe_course(cls, message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            send_available_subjects(chat_id, locale)

        except Exception as e:
            log_exception(chat_id, cls.subscribe_course, e)
