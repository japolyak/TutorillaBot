from ..bot_token import bot
from telebot import types
from ..i18n.i18n import t
from ..decorators import session_checker


@bot.message_handler(regexp='Українська')
@session_checker
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('ua', 'language_changed_to'))


@bot.message_handler(regexp='Polski')
@session_checker
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('pl', 'language_changed_to'))


@bot.message_handler(regexp='Русский')
@session_checker
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('ru', 'language_changed_to'))


@bot.message_handler(regexp='English')
@session_checker
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('en', 'language_changed_to'))
