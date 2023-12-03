from telebot import types
from telebot import service_utils
from bot.i18n.i18n import t
from bot.redis_client import r
from typing import List


class ReplyKeyboardMarkupCreator:
    @staticmethod
    def phone_markup(language: str) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone_btn = types.KeyboardButton(t(language, "phone"), request_contact=True)
        markup.add(phone_btn)

        return markup

    @staticmethod
    def main_menu_markup(user_id) -> types.ReplyKeyboardMarkup:
        is_tutor = int(r.hget(str(user_id), "is_tutor"))
        is_student = int(r.hget(str(user_id), "is_student"))
        is_admin = int(r.hget(str(user_id), "is_admin"))

        markup = CustomReplyKeyboardMarkup(resize_keyboard=True)

        profile_btn = types.KeyboardButton(text="Profile")
        support_btn = types.KeyboardButton(text="Support")
        top_row = []
        if is_tutor:
            office_btn = types.KeyboardButton(text="Office")
            top_row.append(office_btn)

        if is_student:
            my_courses_btn = types.KeyboardButton(text="Classroom")
            top_row.append(my_courses_btn)

        if is_admin:
            my_courses_btn = types.KeyboardButton(text="Admin panel")
            top_row.append(my_courses_btn)

        markup.add_row(top_row)
        markup.add(profile_btn, support_btn)

        return markup

    @staticmethod
    def student_classroom_markup() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        my_courses_btn = types.KeyboardButton(text="My classes")
        add_course_btn = types.KeyboardButton(text="Subscribe course")
        main_menu_btn = types.KeyboardButton(text="Main menu")

        markup.add(my_courses_btn, add_course_btn).add(main_menu_btn)

        return markup

    @staticmethod
    def tutor_office_markup() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        my_courses_btn = types.KeyboardButton(text="My courses")
        add_course_btn = types.KeyboardButton(text="Add course")
        main_menu_btn = types.KeyboardButton(text="Main menu")

        markup.add(my_courses_btn, add_course_btn).add(main_menu_btn)

        return markup


class CustomReplyKeyboardMarkup(types.ReplyKeyboardMarkup):
    def add_row(self, buttons: List[types.KeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = []
            for button in row:
                if service_utils.is_string(button):
                    button_array.append({'text': button})
                elif service_utils.is_bytes(button):
                    button_array.append({'text': button.decode('utf-8')})
                else:
                    button_array.append(button.to_dict())
            self.keyboard.append(button_array)

        return self
