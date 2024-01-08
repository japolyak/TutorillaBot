from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from bot.i18n.i18n import t
from typing import List
from ..api.api_models import SubjectDto, PrivateCourseDto, PrivateClassDto
from ..config import web_app_link

class InlineKeyboardMarkupCreator:
    @staticmethod
    def language_markup(command: str) -> InlineKeyboardMarkup:
        ukr_btn = InlineKeyboardButton("Українська", callback_data=f"{command} ua")
        rus_btn = InlineKeyboardButton("Русский", callback_data=f"{command} ru")
        eng_btn = InlineKeyboardButton("English", callback_data=f"{command} en")
        pol_btn = InlineKeyboardButton("Polski", callback_data=f"{command} pl")

        markup = InlineKeyboardMarkup([[ukr_btn, rus_btn, eng_btn], [pol_btn]])

        return markup

    @staticmethod
    def change_profile(language: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        first_name_btn = InlineKeyboardButton(t(language, "first_name"), callback_data="set first_name")
        last_name_btn = InlineKeyboardButton(t(language, "last_name"), callback_data="set last_name")
        phone_btn = InlineKeyboardButton(t(language, "phone"), callback_data="set phone")
        email_btn = InlineKeyboardButton(t(language, "email"), callback_data="set email")

        markup.add(first_name_btn, last_name_btn).add(phone_btn, email_btn)

        return markup

    @staticmethod
    def choose_occupation() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        # TODO - translate
        teacher_btn = InlineKeyboardButton("Teach", callback_data="BecomeTutor")
        student_btn = InlineKeyboardButton("Study", callback_data="BecomeStudent")

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def tutor_courses_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Tutor {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def student_courses_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Student {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def add_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, callback_data=f"Add course {course.id}"))
            for course
            in courses]

        return markup

    @staticmethod
    def sub_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Subscribe {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def subscribe_course_markup(course_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        subscribe_btn = InlineKeyboardButton("Subscribe", callback_data=f"SubscribeCourse {course_id}")
        return_btn = InlineKeyboardButton("Return to select subjects", callback_data="ReturnToSelect")

        markup.add(subscribe_btn).add(return_btn)

        return markup
