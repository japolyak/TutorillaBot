from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from typing import Any, List


class StudentActions:
    @staticmethod
    def subscribe_course_callback(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            course_id, locale = callback_data

            request = PrivateCourseClient.enroll_in_course(user_id=chat_id, private_course_id=course_id)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Problem occurred", disable_notification=True)
                return

            bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
            markup = ReplyKeyboardMarkupCreator.student_classroom_markup(locale)
            bot.send_message(chat_id=chat_id, text="You have successfully subscribed to the course",
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
