import logging
from src.bot_token import bot
from src.config import debug
from typing import Callable


def log_exception(chat_id: int, func: Callable, e: Exception | None = None, api_error: bool = False):
    logging.error(msg=f"Exception in {func.__name__} action method{" by API side" if api_error else ''}.", exc_info=e)

    if debug:
        error_message = f"Exception in <b>{func.__name__}</b>\n{e if e else ''}"
        bot.send_message(chat_id=chat_id, text=error_message, parse_mode='HTML', disable_notification=True)
        return

    error_message = f"Error Occurred. Try again later."
    bot.send_message(chat_id=chat_id, text=error_message, disable_notification=True)
