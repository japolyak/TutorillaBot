from ..bot_token import bot
from telebot import types
from ..i18n import t


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    ukr_btn = types.KeyboardButton('Українська')
    rus_btn = types.KeyboardButton('Русский')
    eng_btn = types.KeyboardButton('English')
    pol_btn = types.KeyboardButton('Polski')

    markup.add(pol_btn, ukr_btn, rus_btn, eng_btn)

    bot.send_message(chat_id=message.chat.id,
                     text=t('ua', 'welcome', name=message.from_user.first_name),
                     reply_markup=markup)
