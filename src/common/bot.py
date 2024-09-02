import logging
from telebot import ExceptionHandler, TeleBot, apihelper

from src.common.config import admin_tg_id, is_development, bot_token
from src.common.string_utils import StringUtils

log = logging.getLogger(__name__)


class BotExceptionHandler(ExceptionHandler):
    def handle(self, exception: Exception):
        log.exception(msg="Caught an exception: ", exc_info=exception)

        message = StringUtils.create_error_message(exception)

        bot.send_message(chat_id=admin_tg_id, text=message, parse_mode="MarkdownV2")

        return True


if is_development:
    apihelper.API_URL = "https://api.telegram.org/bot{0}/test/{1}"

bot = TeleBot(
    token=bot_token,
    threaded=False,
    disable_notification=True,
    exception_handler=BotExceptionHandler(),
    use_class_middlewares=True
)
