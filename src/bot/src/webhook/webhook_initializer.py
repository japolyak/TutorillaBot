import logging
import time
from telebot import apihelper

from src.common.bot_token import bot
from src.common.config import webhook_url, is_development


log = logging.getLogger(__name__)


def initialize_webhook():
    if is_development:
        apihelper.API_URL = "https://api.telegram.org/bot{0}/test/{1}"

    webhook = bot.get_webhook_info()

    if webhook.url == webhook_url:
        return

    bot.remove_webhook()
    time.sleep(0.1)
    log.info(msg="Webhook removed")

    bot.set_webhook(url=webhook_url)
    log.info(msg="Webhook set up")
