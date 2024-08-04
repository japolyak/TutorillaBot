import logging
from telebot import ExceptionHandler, TeleBot

from src.common.config import dev_tg_id, is_development, bot_token

log = logging.getLogger(__name__)

class CustomExceptionHandler(ExceptionHandler):
    def handle(self, exception: Exception):
        logging.exception(msg="Caught an exception: ", exc_info=exception)

        if is_development:
            bot.send_message(chat_id=dev_tg_id, text=exception.__str__(), disable_notification=True)

        return True


bot = TeleBot(bot_token, threaded=False, exception_handler=CustomExceptionHandler())
