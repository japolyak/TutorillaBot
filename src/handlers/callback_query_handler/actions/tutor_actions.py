from telebot.types import CallbackQuery, Message
from src.bot_token import bot
from src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.handlers.shared import get_subjects, next_stepper
from typing import Any, List
from src.api.api_models import NewTutorCourseDto
from src.api.clients.tutor_course_client import TutorCourseClient
from src.validators import Validator
from src.i18n.i18n import t


class TutorActions:
    @classmethod
    def back_to_choose_subject_callback(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        role, locale = callback_data
        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id)

        get_subjects(chat_id, role, locale)

    @classmethod
    def back_to_private_course(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        private_course_id, inline_message_id, role, locale = callback_data

        markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id, role, locale, chat_id)
        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    @classmethod
    def add_course_callback(cls, call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        subject_id, subject_name, locale = callback_data

        message_id = call.message.message_id

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

        next_stepper(chat_id,
                     t(chat_id, "SpecifyCourseCostPerHourInDollars", locale, subject=subject_name),
                     cls.__add_course_price, locale=locale, parse_mode="HTML", subject_id=subject_id)

    @classmethod
    def __add_course_price(cls, message: Message, **kwargs):
        chat_id = message.from_user.id
        locale = kwargs.get("locale")

        if message.content_type != "text" or not Validator.int_validator(message.text):
            next_stepper(chat_id, t(chat_id, "UseOnlyNumbers", locale), cls.__add_course_price, **kwargs)
            return

        payload = NewTutorCourseDto(subject_id=kwargs.get("subject_id"),
                                    price=int(message.text)).model_dump_json()

        request = TutorCourseClient.add_course(user_id=chat_id, payload=payload)

        if not request.ok:
            bot.send_message(chat_id=chat_id,
                             text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                             disable_notification=True)
            return

        bot.send_message(chat_id=chat_id, text=t(chat_id, "CourseAddedSuccessfully", locale),
                         disable_notification=True)
