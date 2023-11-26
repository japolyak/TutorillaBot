from telebot import types


class MarkupCreator:
    @staticmethod
    def language_markup(command: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=2)

        ukr_btn = types.InlineKeyboardButton("Українська", callback_data=f"{command} ua")
        rus_btn = types.InlineKeyboardButton("Русский", callback_data=f"{command} ru")
        eng_btn = types.InlineKeyboardButton("English", callback_data=f"{command} en")
        pol_btn = types.InlineKeyboardButton("Polski", callback_data=f"{command} pl")

        markup.add(pol_btn, ukr_btn).add(rus_btn, eng_btn)

        return markup
