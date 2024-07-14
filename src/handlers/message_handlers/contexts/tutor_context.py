from telebot.types import Message
from src.api.clients.subject_client import SubjectClient
from src.bot_token import bot
from src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.api.api_models import SubjectDto, Role, ItemsDto
from src.handlers.shared import get_subjects
from src.exception_handler import log_exception
from src.i18n.i18n import t
from src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.redis_service.redis_client import r


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
            get_subjects(chat_id, Role.Tutor, locale)

        except Exception as e:
            log_exception(chat_id, TutorContext.tutor_courses, e)

    @staticmethod
    @__guard
    def add_course(chat_id: int):
        try:
            request = SubjectClient.get_users_subjects(chat_id, Role.Tutor, True)

            if not request.ok:
                log_exception(chat_id, TutorContext.add_course, api_error=True)
                return

            locale = r.hget(chat_id, "locale")

            response_data: ItemsDto[SubjectDto] = ItemsDto[SubjectDto](**request.json())

            if not response_data.items:
                bot.send_message(chat_id=chat_id, text=t(chat_id, "NoAvailableSubjects", locale),
                                 disable_notification=True)
                return

            msg_text = t(chat_id, "ChooseSubjectToTeach", locale)

            markup = InlineKeyboardMarkupCreator.add_course_markup(response_data.items, locale)

            bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, TutorContext.add_course, e)
