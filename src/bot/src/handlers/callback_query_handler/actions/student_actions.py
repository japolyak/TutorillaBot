from telebot.types import CallbackQuery
from typing import Any, List

from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.api.clients.subject_client import SubjectClient

from src.core.bot.bot import bot
from src.core.i18n.i18n import t
from src.core.models import Role
from src.core.bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.core.bot.enums import InlineQueryParam


class StudentActions:
    @staticmethod
    def to_classroom(call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        locale, *_ = callback_data
        chat_id = call.from_user.id
        message_id = call.message.message_id

        markup = InlineKeyboardMarkupCreator.classroom_markup(chat_id, locale, is_student=True)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=t(chat_id, "YourClassroomIsHere", locale),
            reply_markup=markup
        )

    @staticmethod
    def find_tutor(call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        locale, *_ = callback_data
        chat_id = call.from_user.id
        message_id = call.message.message_id

        response = SubjectClient.get_available_subjects(tg_data=call)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            subjects = []
            text = "NoAvailableTutors"
        else:
            subjects = response.data.items
            text = "ChooseSubjectIKBtn"

        markup = InlineKeyboardMarkupCreator.subjects_markup(subjects, Role.Student, InlineQueryParam.Tutors, chat_id, locale)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=t(chat_id, text, locale),
                              reply_markup=markup)

    @classmethod
    def subscribe_course(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id
        course_id, locale = callback_data

        response = TutorCourseClient.enroll_in_course(course_id, tg_data=call)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
        bot.send_message(chat_id=chat_id, text=t(chat_id, "YouHaveSuccessfullySubscribedToTheCourse", locale))

    @staticmethod
    def return_to_select(call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id
        locale, *_ = callback_data

        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)

        response = SubjectClient.get_available_subjects(tg_data=call)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            bot.send_message(chat_id=chat_id, text=t(chat_id, "NoAvailableTutors", locale))
            return

        markup = InlineKeyboardMarkupCreator.subjects_markup(response.data.items, Role.Student, InlineQueryParam.Tutors,
                                                             chat_id, locale)

        bot.send_message(chat_id=chat_id,
                              text=t(chat_id, "ChooseSubjectIKBtn", locale),
                              reply_markup=markup)
