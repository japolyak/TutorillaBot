from telebot.types import CallbackQuery
from src.bot.apiold.clients.private_course_client import PrivateCourseClient
from src.bot.bot_token import bot
from src.bot.handlers.shared import send_available_subjects
from src.bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.exception_handler import log_exception
from typing import Any, List
from src.bot.i18n.i18n import t


class StudentActions:
    @classmethod
    def subscribe_course_callback(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            course_id, locale = callback_data

            request = PrivateCourseClient.enroll_in_course(user_id=chat_id, private_course_id=course_id)

            if not request.ok:
                log_exception(chat_id, cls.subscribe_course_callback, api_error=True)
                return

            bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
            markup = ReplyKeyboardMarkupCreator.student_classroom_markup(chat_id, locale)
            bot.send_message(chat_id=chat_id, text=t(chat_id, "YouHaveSuccessfullySubscribedToTheCourse", locale),
                             disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, StudentActions.subscribe_course_callback, e)

    @staticmethod
    def return_to_select_callback(call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        try:
            locale = callback_data[0]

            bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
            send_available_subjects(chat_id, locale)

        except Exception as e:
            log_exception(chat_id, StudentActions.return_to_select_callback, e)
