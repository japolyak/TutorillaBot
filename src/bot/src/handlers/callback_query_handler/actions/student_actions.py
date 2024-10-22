from telebot.types import CallbackQuery
from typing import Any, List

from src.common.bot import bot

from src.bot.src.handlers.shared import Shared
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.private_course_client import PrivateCourseClient
from src.bot.src.services.i18n.i18n import t


class StudentActions:
    @classmethod
    def subscribe_course_callback(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        course_id, locale = callback_data

        response = PrivateCourseClient.enroll_in_course(user_id=chat_id, private_course_id=course_id)

        if not response.ok:
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
        markup = ReplyKeyboardMarkupCreator.student_classroom_markup(chat_id, locale)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "YouHaveSuccessfullySubscribedToTheCourse", locale),
                         reply_markup=markup)

    @staticmethod
    def return_to_select_callback(call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        locale = callback_data[0]

        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
        Shared.send_available_subjects(chat_id, locale)
