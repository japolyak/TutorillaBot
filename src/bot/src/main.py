import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.core.bot.bot import bot
from src.core.logger import log
from src.core.redis_configuration import redis_instance as r

from src.bot.src.handlers.callback_query_handler import callback_query_handler
from src.bot.src.handlers.inline_handler import inline_handler
from src.bot.src.handlers.message_handlers import message_handler, registration

from src.bot.src.middlewares import MessageMiddleware, RedisMiddleware, InlineQueryMiddleware, StateMiddleware

log.info(msg="Starting bot...")

bot.setup_middleware(MessageMiddleware())
bot.setup_middleware(InlineQueryMiddleware())
bot.setup_middleware(RedisMiddleware(r))
# necessary for state parameter in handlers.
bot.setup_middleware(StateMiddleware(bot))

log.info(msg='Starting polling')

logging.getLogger("urllib3").setLevel(logging.CRITICAL)

bot.infinity_polling()
