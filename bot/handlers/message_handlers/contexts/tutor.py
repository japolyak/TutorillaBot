from telebot.types import Message
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator
from bot.i18n.i18n import t
from bot.redis.redis_client import r


class Tutor:
    @staticmethod
    def my_office(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.tutor_office_markup(locale)
            bot.send_message(chat_id=chat_id,text=t(chat_id, "OfficeIsHere", locale),
                             disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, Tutor.my_office, e)

    @staticmethod
    def tutor_courses(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            locale = r.hget(chat_id, "locale")
            get_subjects(chat_id, "tutor", locale)

        except Exception as e:
            log_exception(chat_id, Tutor.tutor_courses, e)

    @staticmethod
    def add_course(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.tutor_guard(chat_id):
                return

            request = SubjectClient.get_available_subjects(user_id=chat_id, role="tutor")

            if not request.ok:
                log_exception(chat_id, Tutor.add_course, api_error=True)
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
            log_exception(chat_id, Tutor.add_course, e)
