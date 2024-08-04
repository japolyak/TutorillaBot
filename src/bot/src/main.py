import logging
import time

from src.common.bot_token import bot
from src.common.config import webhook_enabled, webhook_url
from src.common.logger import configure_logger

log = logging.getLogger(__name__)

configure_logger()

log.info(msg="Starting bot...")


def init_webhook():
    webhook = bot.get_webhook_info()

    if webhook.url != webhook_url:
        bot.remove_webhook()
        time.sleep(0.1)

        bot.set_webhook(url=webhook_url)


if webhook_enabled:
    init_webhook()
else:
    logging.info('Removing webhook..')
    bot.remove_webhook()
    time.sleep(0.1)

    logging.info('Initializing handlers')

    logging.info('Starting polling')

    bot.infinity_polling()
