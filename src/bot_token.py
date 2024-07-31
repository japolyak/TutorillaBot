import logging
import telebot
from telebot import ExceptionHandler
from src.config import token
from src.config import is_development, dev_tg_id


class CustomExceptionHandler(ExceptionHandler):
    def handle(self, exception: Exception):
        logging.exception(msg="Caught an exception: ", exc_info=exception)

        if is_development:
            bot.send_message(chat_id=dev_tg_id, text=exception.__str__(), disable_notification=True)

        return True


bot = telebot.TeleBot(token, threaded=False, exception_handler=CustomExceptionHandler())
