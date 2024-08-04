import time

from src.common.bot_token import bot
from src.common.config import webhook_url


def initialize_webhook():
    webhook = bot.get_webhook_info()

    if webhook.url == webhook_url:
        return

    bot.remove_webhook()
    time.sleep(0.1)

    bot.set_webhook(url=webhook_url)
