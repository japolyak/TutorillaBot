from telebot.types import Message
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator


class Tutor:
    @staticmethod
    def my_office(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
            bot.send_message(chat_id=chat_id, text="Office is here", disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Tutor.my_office, e)

    @staticmethod
    def tutor_courses(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            get_subjects(chat_id, "tutor")

        except Exception as e:
            log_exception(chat_id, Tutor.tutor_courses, e)

    @staticmethod
    def add_course(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            request = SubjectClient.get_available_subjects(user_id=chat_id, role="tutor")

            if not len(request.json()):
                bot.send_message(chat_id=chat_id, text="No available subjects", disable_notification=True)
                return

            response_data = [SubjectDto(**s) for s in request.json()]

            if not len(response_data):
                bot.send_message(chat_id=chat_id, text="No available subjects", disable_notification=True)
                return

            msg_text = "Choose course to teach"

            markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

            bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Tutor.add_course, e)
