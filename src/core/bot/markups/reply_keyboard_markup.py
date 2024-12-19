from telebot import service_utils
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from src.core.i18n.i18n import t


class ReplyKeyboardMarkupCreator:
    @staticmethod
    def welcome_markup(user_id, locale, *args, **kwargs) -> ReplyKeyboardMarkup:
        markup = CustomReplyKeyboardMarkup(resize_keyboard=True)

        top_row = []

        if kwargs["is_admin"]:
            btn = KeyboardButton(text=t(user_id, "AdminPanelKBtn", locale))
            top_row.append(btn)

        if kwargs["is_student"] or kwargs["is_tutor"]:
            btn = KeyboardButton(text=t(user_id, "ClassroomKBtn", locale))
            top_row.append(btn)

        if top_row.__len__() > 0: markup.add_row(top_row)

        profile = KeyboardButton(text="Profile")
        support = KeyboardButton(text="Support")

        markup.add(profile).add(support)

        return markup


class CustomReplyKeyboardMarkup(ReplyKeyboardMarkup):
    def add_row(self, buttons: List[KeyboardButton], row_width=None):
        if row_width is None: row_width = self.row_width

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
