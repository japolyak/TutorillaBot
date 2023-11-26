from ..bot_token import bot
from telebot import types
from ..i18n.i18n import t


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    ukr_btn = types.InlineKeyboardButton("Українська", callback_data="set ua")
    rus_btn = types.InlineKeyboardButton("Русский", callback_data="set ru")
    eng_btn = types.InlineKeyboardButton("English", callback_data="set en")
    pol_btn = types.InlineKeyboardButton("Polski", callback_data="set pl")

    markup.add(pol_btn, ukr_btn).add(rus_btn, eng_btn)

    bot.send_message(chat_id=message.chat.id,
                     text="Hello! Feel free to adjust your language settings with the options provided.",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data == "set ua" or
                                               call.data == "set ru" or
                                               call.data == "set pl" or
                                               call.data == "set en"))
def set_language(call: types.CallbackQuery):
    _, language = call.data.split(" ")
    text = t(language, 'language_changed_to')

    bot.send_message(chat_id=call.from_user.id, text=text)
