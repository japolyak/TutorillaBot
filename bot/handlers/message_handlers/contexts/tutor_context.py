from telebot.types import Message
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.i18n.i18n import t
from bot.handlers.message_handlers.contexts.i_context_base import IContextBase
from bot.redis.redis_client import r


class TutorContext(IContextBase):
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
            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.tutor_office_markup(chat_id, locale)
            bot.send_message(chat_id=chat_id, text=t(chat_id, "OfficeIsHere", locale),
                             disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, TutorContext.my_office, e)

    @staticmethod
    @__guard
    def tutor_courses(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            get_subjects(chat_id, "tutor", locale)

        except Exception as e:
            log_exception(chat_id, TutorContext.tutor_courses, e)

    @staticmethod
    @__guard
    def add_course(chat_id: int):
        try:
            request = SubjectClient.get_available_subjects(user_id=chat_id, role="tutor")

            if not request.ok:
                log_exception(chat_id, TutorContext.add_course, api_error=True)
                return

            locale = r.hget(chat_id, "locale")
            if not len(request.json()):
                bot.send_message(chat_id=chat_id, text=t(chat_id, "NoAvailableSubjects", locale),
                                 disable_notification=True)
                return

            response_data = [SubjectDto(**s) for s in request.json()]

            msg_text = t(chat_id, "ChooseSubjectToTeach", locale)

            markup = InlineKeyboardMarkupCreator.add_course_markup(response_data, locale)

            bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, TutorContext.add_course, e)
