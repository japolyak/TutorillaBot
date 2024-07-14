from src.bot_token import bot
from src.config import webhook_enabled, webhook_url, app_port
from src.webhook_app import app
import logging
import time
import uvicorn
from src.handlers.callback_query_handler import query_handler
from src.handlers.inline_handler import inline_handler
from src.handlers.message_handlers import message_handler, registration

logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


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
        logging.info('Starting src..')

        logging.info('Removing webhook..')
        bot.remove_webhook()
        time.sleep(0.1)

        logging.info('Initializing handlers')

        logging.info('Starting polling')

        bot.infinity_polling()
