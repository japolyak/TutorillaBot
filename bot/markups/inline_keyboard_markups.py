from telebot import types
from bot.i18n.i18n import t
from typing import List
from ..api.api_models import Subject


class InlineKeyboardMarkupCreator:
    @staticmethod
    def language_markup(command: str) -> types.InlineKeyboardMarkup:
        ukr_btn = types.InlineKeyboardButton("Українська", callback_data=f"{command} ua")
        rus_btn = types.InlineKeyboardButton("Русский", callback_data=f"{command} ru")
        eng_btn = types.InlineKeyboardButton("English", callback_data=f"{command} en")
        pol_btn = types.InlineKeyboardButton("Polski", callback_data=f"{command} pl")

        markup = types.InlineKeyboardMarkup([[ukr_btn, rus_btn, eng_btn], [pol_btn]])

        return markup

    @staticmethod
    def change_profile(language: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        first_name_btn = types.InlineKeyboardButton(t(language, "first_name"), callback_data="set first_name")
        last_name_btn = types.InlineKeyboardButton(t(language, "last_name"), callback_data="set last_name")
        phone_btn = types.InlineKeyboardButton(t(language, "phone"), callback_data="set phone")
        email_btn = types.InlineKeyboardButton(t(language, "email"), callback_data="set email")

        markup.add(first_name_btn, last_name_btn).add(phone_btn, email_btn)

        return markup

    @staticmethod
    def choose_occupation() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        # TODO - translate
        teacher_btn = types.InlineKeyboardButton("Teacher", callback_data="tutor")
        student_btn = types.InlineKeyboardButton("Student", callback_data="student")

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def tutor_courses_markup(courses: List[Subject]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        [markup.add(
            types.InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Tutor {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def student_courses_markup(courses: List[Subject]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        [markup.add(
            types.InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Student {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def add_course_markup(courses: List[Subject]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        [markup.add(
            types.InlineKeyboardButton(text=course.name, callback_data=f"Add course {course.id}"))
            for course
            in courses]

        return markup

    @staticmethod
    def sub_course_markup(courses: List[Subject]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        [markup.add(
            types.InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Subscribe {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def subscribe_course_markup(course_id: int) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        subscribe_btn = types.InlineKeyboardButton("Subscribe", callback_data=f"Subscribe course {course_id}")
        return_btn = types.InlineKeyboardButton("Return to select subjects", callback_data="Return to select")

        markup.add(subscribe_btn).add(return_btn)

        return markup
