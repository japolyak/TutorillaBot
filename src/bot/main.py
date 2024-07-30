from src.bot.bot_token import bot
from src.bot.config import webhook_enabled, webhook_url, app_port
from src.bot.webhook_app import app
from src.bot.logger import configure_logging
import time
import uvicorn
import logging

from src.bot.handlers.callback_query_handler import query_handler
from src.bot.handlers.inline_handler import inline_handler
from src.bot.handlers.message_handlers import message_handler, registration

# logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

log = logging.getLogger(__name__)

# Logging level and format configuration
configure_logging()

log.info(msg="Starting app...")


def init_webhook():
    webhook = bot.get_webhook_info()

    if webhook.url != webhook_url:
        bot.remove_webhook()
        time.sleep(0.1)

        bot.set_webhook(url=webhook_url)


if webhook_enabled:
    init_webhook()

if __name__ == '__main__':
    # Does not run on production
    if webhook_enabled:
        init_webhook()
        uvicorn.run(app, host="0.0.0.0", port=app_port)
    else:
        log.info(msg='Starting src..')

        log.info(msg='Removing webhook..')
        bot.remove_webhook()
        time.sleep(0.1)

        log.info(msg='Initializing handlers')

        log.info(msg='Starting polling')

        bot.infinity_polling()
