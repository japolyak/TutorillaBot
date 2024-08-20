from telebot.types import Message

from src.common.bot import bot
from src.common.models import SubjectDto, Role, ItemsDto

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.handlers.shared import get_subjects
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.subject_client import SubjectClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_client import r


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
        locale = r.hget(chat_id, "locale")
        markup = ReplyKeyboardMarkupCreator.tutor_office_markup(chat_id, locale)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "OfficeIsHere", locale),
                         disable_notification=True, reply_markup=markup)

    @staticmethod
    @__guard
    def tutor_courses(chat_id: int):
        locale = r.hget(chat_id, "locale")
        get_subjects(chat_id, Role.Tutor, locale)

    @staticmethod
    @__guard
    def add_course(chat_id: int):
        request = SubjectClient.get_users_subjects(chat_id, Role.Tutor, True)

        if not request.ok:
            bot.send_message(chat_id=chat_id,
                             text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                             disable_notification=True)
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