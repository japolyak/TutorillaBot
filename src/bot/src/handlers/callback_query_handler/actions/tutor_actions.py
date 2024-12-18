from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from typing import Any, List, Optional
from telebot.states.sync.context import StateContext

from src.core.bot import bot
from src.core.models import NewTutorCourseDto, ItemsDto

from src.bot.src.handlers.shared import Shared
from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.api.clients.textbook_client import TextbookClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.states import TextbookState
from src.bot.src.validators import Validator


class TutorActions:
    @classmethod
    def back_to_choose_subject_callback(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        role, locale = callback_data
        bot.edit_message_reply_markup(inline_message_id=call.inline_message_id)

        Shared.get_subjects(chat_id, locale, role, "Courses")

    @classmethod
    def back_to_private_course(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        private_course_id, inline_message_id, role, locale = callback_data

        markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id, role, locale, chat_id)
        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    @classmethod
    def add_course_callback(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        chat_id = call.from_user.id

        subject_id, subject_name, locale = callback_data

        message_id = call.message.message_id

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

        Shared.next_stepper(chat_id,
                     t(chat_id, "SpecifyCourseCostPerHourInDollars", locale, subject=subject_name),
                     cls.__add_course_price, locale=locale, parse_mode="HTML", subject_id=subject_id)

    @classmethod
    def tutor_course_panel(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        user_id = call.from_user.id
        course_id, locale = callback_data
        message_id = call.message.message_id

        # TODO - Add request to get info about the course
        markup = InlineKeyboardMarkupCreator.course_markup(user_id, locale, course_id)
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Your course - rewrite", reply_markup=markup)

    @classmethod
    def back_to_office(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        user_id = call.from_user.id
        message_id = call.message.message_id
        locale = callback_data[0]

        bot.delete_message(chat_id=user_id, message_id=message_id)

        markup = ReplyKeyboardMarkupCreator.tutor_office_markup(user_id, locale)
        bot.send_message(chat_id=user_id, text=t(user_id, "OfficeIsHere", locale),
                         reply_markup=markup)

    @classmethod
    def back_to_courses(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        user_id = call.from_user.id
        locale = callback_data[0]
        message_id = call.message.message_id

        Shared.get_courses_for_panel(user_id, locale, False, message_id)

    @classmethod
    def load_course_textbooks(cls, call: CallbackQuery, callback_data: List[Any], *args, **kwargs):
        user_id = call.from_user.id
        locale, course_id = callback_data
        message_id = call.message.message_id

        response = TextbookClient.get_textbooks(course_id)

        if not response.is_successful():
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        markup = InlineKeyboardMarkupCreator.textbooks_markup(user_id, locale, course_id, response.data.items)

        bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Here your textbooks", reply_markup=markup)

    @classmethod
    def add_textbooks(cls, call: CallbackQuery, callback_data: List[Any], state: StateContext,  *args, **kwargs):
        user_id = call.from_user.id
        locale, tutor_course_id = callback_data

        state.add_data(tutor_course_id=tutor_course_id)
        state.set(TextbookState.first_textbook)

        markup = ReplyKeyboardRemove()

        bot.send_message(chat_id=user_id, text="Add textbooks", reply_markup=markup)

    @classmethod
    def save_textbooks(cls, call: CallbackQuery, callback_data: List[Any], state: StateContext,  *args, **kwargs):
        user_id = call.from_user.id
        locale = callback_data[0]

        with state.data() as data:
            tutor_course_id: Optional[int] = data.get("tutor_course_id")
            textbooks: Optional[List[str]] = data.get("textbooks")

        if tutor_course_id is None or textbooks is None:
            # TODO - finish later
            print('Return')

        payload = ItemsDto[str](items=textbooks)

        response = TextbookClient.save_textbooks(tutor_course_id, payload)

        if not response.is_successful():
            # TODO - add markup
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        state.set('')

        message_id = call.message.message_id

        bot.delete_message(chat_id=user_id, message_id=message_id)

        markup = InlineKeyboardMarkupCreator.course_markup(user_id, locale, tutor_course_id)
        bot.send_message(chat_id=user_id, text="Your course - rewrite", reply_markup=markup)

    @classmethod
    def __add_course_price(cls, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        locale = kwargs.get("locale")

        if message.content_type != "text" or not Validator.int_validator(message.text):
            Shared.next_stepper(user_id, t(user_id, "UseOnlyNumbers", locale), cls.__add_course_price, **kwargs)
            return

        payload = NewTutorCourseDto(subject_id=kwargs.get("subject_id"),
                                    price=int(message.text)).model_dump_json()

        response = TutorCourseClient.add_course(user_id=user_id, payload=payload)

        if not response.ok:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        bot.send_message(chat_id=user_id, text=t(user_id, "CourseAddedSuccessfully", locale))
