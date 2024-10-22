import logging
import time

from src.common.bot import bot
from src.common.config import webhook_url


log = logging.getLogger(__name__)


def initialize_webhook():
    webhook = bot.get_webhook_info()

    if webhook.url == webhook_url:
        return

    bot.remove_webhook()
    time.sleep(0.1)
    log.info(msg="Webhook removed")

    bot.set_webhook(url=webhook_url)
    log.info(msg="Webhook set up")
