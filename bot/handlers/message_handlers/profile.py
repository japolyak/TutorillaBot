from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception


@bot.message_handler(regexp="Main menu")
def main_menu(message: Message):
    chat_id = message.from_user.id

    try:
        markup = ReplyKeyboardMarkupCreator.main_menu_markup(chat_id)
        bot.send_message(chat_id=chat_id, text="Main menu", disable_notification=True, reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, main_menu, e)
