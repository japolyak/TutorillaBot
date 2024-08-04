import logging
import time

from src.common.bot_token import bot
from src.common.config import is_development
from src.common.logger import configure_logger

from src.bot.src.webhook.webhook_initializer import initialize_webhook

from src.bot.src.handlers.callback_query_handler import query_handler
from src.bot.src.handlers.inline_handler import inline_handler
from src.bot.src.handlers.message_handlers import message_handler, registration


log = logging.getLogger(__name__)

configure_logger()

log.info(msg="Starting bot...")


if not is_development:
    initialize_webhook()
else:
    log.info(msg='Removing webhook..')

    bot.remove_webhook()
    time.sleep(0.1)

    log.info(msg='Starting polling')

    bot.infinity_polling()
