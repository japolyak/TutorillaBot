from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator


class MainView:
    @staticmethod
    def main_menu(message: Message):
        chat_id = message.from_user.id

        try:
            if not MessageDecorator.main_view_guard(chat_id):
                return

            markup = ReplyKeyboardMarkupCreator.main_menu_markup(chat_id)
            bot.send_message(chat_id=chat_id, text="Main menu", disable_notification=True, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, MainView.main_menu, e)
