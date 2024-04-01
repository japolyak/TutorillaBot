from telebot.types import CallbackQuery, Message
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.handlers.shared import get_subjects, next_stepper
from bot.exception_handler import log_exception
from typing import Any, List
from bot.i18n.i18n import t
from bot.api.api_models import NewTutorCourseDto
from bot.api.clients.tutor_course_client import TutorCourseClient
from bot.validators import Validator


class TutorActions:
    @classmethod
    def back_to_choose_subject_callback(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            role = callback_data[0]

            get_subjects(chat_id, role)

        except Exception as e:
            log_exception(chat_id, cls.back_to_choose_subject_callback, e)

    @classmethod
    def back_to_private_course(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            private_course_id, inline_message_id, role = callback_data

            request = PrivateCourseClient.get_private_course(user_id=chat_id, private_course_id=private_course_id)

            if not request.ok:
                bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)

            markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id=private_course_id, role=role)
            bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, cls.back_to_private_course, e)

    @classmethod
    def add_course_callback(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            subject_id, subject_name = callback_data

            message_id = call.message.message_id

            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

            next_stepper(chat_id,
                         t(int(chat_id), "SpecifyCourseCostPerHourInDollars", "en-US", subject=f"{subject_name}"),
                         cls.__add_course_price, locale="en-US", parse_mode="HTML", subject_id=subject_id)

        except Exception as e:
            log_exception(chat_id, cls.add_course_callback, e)

    @classmethod
    def __add_course_price(cls, message: Message, **kwargs):
        chat_id = message.from_user.id

        try:
            if message.content_type != "text" or not Validator.int_validator(message.text):
                next_stepper(chat_id, t(int(chat_id), "UseOnlyNumbers", "en-US"), cls.__add_course_price, **kwargs)
                return

            payload = NewTutorCourseDto(subject_id=kwargs.get("subject_id"),
                                        price=int(message.text)).model_dump_json()

            request = TutorCourseClient.add_course(user_id=chat_id, payload=payload)

            if not request.ok:
                log_exception(chat_id, cls.__add_course_price, api_error=True)

                return

            bot.send_message(chat_id=chat_id, text=t(int(chat_id), "CourseAddedSuccessfully", "en-US"), disable_notification=True)

        except Exception as e:
            log_exception(chat_id, cls.__add_course_price, e)
