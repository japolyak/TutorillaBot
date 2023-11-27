from telebot import types
from .i18n.i18n import t


class MarkupCreator:
    """
    Markups creator
    """
    @staticmethod
    def language_markup(command: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        ukr_btn = types.InlineKeyboardButton("Українська", callback_data=f"{command} ua")
        rus_btn = types.InlineKeyboardButton("Русский", callback_data=f"{command} ru")
        eng_btn = types.InlineKeyboardButton("English", callback_data=f"{command} en")
        pol_btn = types.InlineKeyboardButton("Polski", callback_data=f"{command} pl")

        markup.add(pol_btn, ukr_btn).add(rus_btn, eng_btn)

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
    def phone_markup(language: str) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone_btn = types.KeyboardButton(t(language, "phone"), request_contact=True)
        markup.add(phone_btn)

        return markup

    @staticmethod
    def choose_occupation(language: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()

        # TODO - translate
        teacher_btn = types.InlineKeyboardButton("Teacher", callback_data="teacher")
        student_btn = types.InlineKeyboardButton("Student", callback_data="student")

        markup.add(teacher_btn, student_btn)

        return markup

    # TODO - delete later
    @staticmethod
    def restore_redis_markup() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        restore_btn = types.KeyboardButton(text="Restore")
        markup.add(restore_btn)

        return markup
