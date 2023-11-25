from ..bot_token import bot
from telebot import types
from ..i18n import t


@bot.message_handler(regexp='Українська')
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('ua', 'language_changed', language='українську'))


@bot.message_handler(regexp='Polski')
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('pl', 'language_changed', language='polski'))


@bot.message_handler(regexp='Русский')
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('ru', 'language_changed', language='русский'))


@bot.message_handler(regexp='English')
def send_lang(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=t('en', 'language_changed', language='english'))
