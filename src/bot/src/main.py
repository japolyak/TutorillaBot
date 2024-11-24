import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.common.bot import bot
# from src.common.config import use_webhook
from src.common.redis_configuration import redis_instance as r
from src.common.logger import configure_logger

# from src.bot.src.webhook.webhook_app import app
# from src.bot.src.webhook.webhook_initializer import initialize_webhook

from src.bot.src.handlers.callback_query_handler import callback_query_handler
from src.bot.src.handlers.inline_handler import inline_handler
from src.bot.src.handlers.message_handlers import message_handler, registration

from src.bot.src.middlewares import MessageMiddleware, RedisMiddleware, InlineQueryMiddleware, StateMiddleware


log = logging.getLogger(__name__)

configure_logger()

log.info(msg="Starting bot...")

bot.setup_middleware(MessageMiddleware())
bot.setup_middleware(InlineQueryMiddleware())
bot.setup_middleware(RedisMiddleware(r))
# necessary for state parameter in handlers.
bot.setup_middleware(StateMiddleware(bot))

# if use_webhook:
#     initialize_webhook()
# else:
#     log.info(msg='Removing webhook..')
#
#     bot.remove_webhook()
#
#     log.info(msg='Starting polling')
#
#     bot.infinity_polling()

log.info(msg='Starting polling')

bot.infinity_polling()
