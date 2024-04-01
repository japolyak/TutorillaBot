from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator


class Student:
    @staticmethod
    def open_classroom(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            markup = ReplyKeyboardMarkupCreator.student_classroom_markup()

            bot.send_message(chat_id=chat_id,
                             text="Your classroom is here",
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Student.open_classroom, e)

    @staticmethod
    def student_courses(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            get_subjects(chat_id, "student")

        except Exception as e:
            log_exception(chat_id, Student.student_courses, e)

    @staticmethod
    def subscribe_course(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.student_guard(chat_id):
                return

            send_available_subjects(user_id=chat_id)

        except Exception as e:
            log_exception(chat_id, Student.subscribe_course, e)
