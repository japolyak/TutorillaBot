import logging
from telebot import ExceptionHandler, TeleBot, apihelper
from telebot.storage import StateRedisStorage

from .config import admin_tg_id, is_development, bot_token, redis_host, redis_db, redis_password, redis_username
from .string_utils import StringUtils

log = logging.getLogger(__name__)


class BotExceptionHandler(ExceptionHandler):
    def handle(self, exception: Exception):
        log.exception(msg="Caught an exception: ", exc_info=exception)

        message = StringUtils.create_error_message(exception)

        bot.send_message(chat_id=admin_tg_id, text=message, parse_mode="MarkdownV2", disable_notification=False)

        return True


if is_development:
    apihelper.API_URL = "https://api.telegram.org/bot{0}/test/{1}"

state_storage = StateRedisStorage(
    host=redis_host,
    db=redis_db,
    password=redis_password
) if redis_username is not None else None

bot = TeleBot(
    token=bot_token,
    threaded=False,
    state_storage=state_storage,
    disable_notification=True,
    exception_handler=BotExceptionHandler(),
    use_class_middlewares=True
)
