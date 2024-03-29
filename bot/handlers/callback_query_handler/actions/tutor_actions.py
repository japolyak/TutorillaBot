from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from typing import Any, List
from bot.api.api_models import SubjectDto
from bot.api.clients.tutor_course_client import TutorCourseClient
from bot.api.clients.subject_client import SubjectClient


class TutorActions:
    @staticmethod
    def back_to_choose_subject_callback(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role = callback_data[0]

            get_subjects(chat_id, role)

        except Exception as e:
            log_exception(chat_id, TutorActions.back_to_choose_subject_callback, e)

    @staticmethod
    def back_to_private_course(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            private_course_id, inline_message_id, role = callback_data

            request = PrivateCourseClient.get_private_course(user_id=chat_id, private_course_id=private_course_id)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)

            markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id=private_course_id, role=role)
            bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, TutorActions.back_to_private_course, e)

    @staticmethod
    def add_course_callback(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            subject_id: int = callback_data[0]

            request = TutorCourseClient.add_course(user_id=call.from_user.id, subject_id=subject_id)

            if not request.ok:
                request = SubjectClient.get_available_subjects(user_id=call.from_user.id, role="tutor")

                response_data = [SubjectDto(**s) for s in request.json()]

                markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)
                bot.send_message(chat_id=call.from_user.id, text="Oops, try again or try later",
                                 disable_notification=True, reply_markup=markup)
                return

            bot.send_message(chat_id=call.from_user.id, text="Course added successfully", disable_notification=True)

        except Exception as e:
            log_exception(chat_id, TutorActions.add_course_callback, e)
