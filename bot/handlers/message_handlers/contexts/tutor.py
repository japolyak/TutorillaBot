from telebot.types import Message
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.i18n.i18n import t
from bot.handlers.message_handlers.contexts.i_base import IBase
from bot.redis.redis_client import r


class Tutor(IBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message):
            is_tutor = r.hget(message.from_user.id, "is_tutor")
            if is_tutor == "1":
                return func(message.from_user.id)

        return wrapper

    @staticmethod
    @__guard
    def my_office(chat_id: int):
        try:
            markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
            bot.send_message(chat_id=chat_id, text="Office is here", disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Tutor.my_office, e)

    @staticmethod
    @__guard
    def tutor_courses(chat_id: int):
        try:
            get_subjects(chat_id, "tutor")

        except Exception as e:
            log_exception(chat_id, Tutor.tutor_courses, e)

    @staticmethod
    @__guard
    def add_course(chat_id: int):
        try:
            request = SubjectClient.get_available_subjects(user_id=chat_id, role="tutor")

            if not request.ok:
                log_exception(chat_id, Tutor.add_course)
                return

            if not len(request.json()):
                bot.send_message(chat_id=chat_id, text="No available subjects", disable_notification=True)
                return

            response_data = [SubjectDto(**s) for s in request.json()]

            msg_text = t(chat_id, "ChooseSubjectToTeach", "en-US")

            markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

            bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Tutor.add_course, e)
