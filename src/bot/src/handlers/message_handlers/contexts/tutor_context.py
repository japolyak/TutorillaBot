from redis import Redis
from telebot.types import Message

from src.common.bot import bot
from src.common.models import Role

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.handlers.shared import Shared
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.subject_client import SubjectClient
from src.bot.src.services.i18n.i18n import t


class TutorContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis, *args, **kwargs):
            user_id = message.from_user.id
            is_tutor = redis.hget(user_id, "is_tutor")

            if is_tutor == "1":
                return func(user_id, redis)

        return wrapper

    @staticmethod
    @__guard
    def my_office(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        markup = ReplyKeyboardMarkupCreator.tutor_office_markup(user_id, locale)
        bot.send_message(chat_id=user_id, text=t(user_id, "OfficeIsHere", locale), reply_markup=markup)

    @staticmethod
    @__guard
    def tutor_students(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        Shared.get_subjects(user_id, locale, Role.Tutor, "Students")

    @staticmethod
    @__guard
    def tutor_courses(user_id: int, redis: Redis, *args, **kwargs):
        locale = redis.hget(user_id, "locale")
        Shared.get_courses_for_panel(user_id, locale)

    @staticmethod
    @__guard
    def add_course(user_id: int, redis: Redis, *args, **kwargs):
        response = SubjectClient.get_users_subjects(user_id, Role.Tutor, True)

        locale = redis.hget(user_id, "locale")

        if not response.is_successful:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        subjects = response.data.items

        if not subjects:
            bot.send_message(chat_id=user_id, text=t(user_id, "NoAvailableSubjects", locale))
            return

        msg_text = t(user_id, "ChooseSubjectToTeach", locale)

        markup = InlineKeyboardMarkupCreator.add_course_markup(subjects, locale)

        bot.send_message(chat_id=user_id, text=msg_text, reply_markup=markup)