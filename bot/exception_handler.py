import logging
from bot.bot_token import bot
from bot.config import debug


def log_exception(chat_id: int, handler_name: str, e: Exception | None = None):
    logging.error(msg=f"Exception in {handler_name} handler", exc_info=e)

    if debug:
        error_message = f"Exception in {handler_name}\n{e}"
        bot.send_message(chat_id=chat_id, text=error_message, disable_notification=True)
        return

    error_message = f"Error Occurred. Try again later."
    bot.send_message(chat_id=chat_id, text=error_message, disable_notification=True)
