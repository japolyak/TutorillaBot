# from bot.bot_token import bot
# from telebot import types
# from bot.i18n.i18n import t
# from bot.decorators import language_message_checker


# @bot.message_handler(regexp='Українська')
# @language_message_checker
# def send_lang(message: types.Message):
#     bot.send_message(chat_id=message.chat.id, text=t('ua', 'language_changed_to'))
#
#
# @bot.message_handler(regexp='Polski')
# @language_message_checker
# def send_lang(message: types.Message):
#     bot.send_message(chat_id=message.chat.id, text=t('pl', 'language_changed_to'))
#
#
# @bot.message_handler(regexp='Русский')
# @language_message_checker
# def send_lang(message: types.Message):
#     bot.send_message(chat_id=message.chat.id, text=t('ru', 'language_changed_to'))
#
#
# @bot.message_handler(regexp='English')
# @language_message_checker
# def send_lang(message: types.Message):
#     bot.send_message(chat_id=message.chat.id, text=t('en', 'language_changed_to'))
