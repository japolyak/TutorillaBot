from redis import Redis
from telebot.handler_backends import BaseMiddleware
from telebot.types import Message, InlineQuery
from telebot.util import update_types

from src.bot.src.handlers.message_handlers.commands import translations


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis_client: Redis):
        self.r = redis_client
        self.update_types = update_types

    def pre_process(self, message: Message, data):
        data["redis"] = self.r

    def post_process(self, message, data, exception=None):
        pass


class MessageMiddleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ["message"]

    def pre_process(self, message: Message, data):
        if message.text.startswith("/"):
            return

        data["command"] = None

        for _, commands in translations.items():
            command_name = commands.get(message.text)
            if command_name:
                data["command"] = command_name

    def post_process(self, message, data, exception=None):
        pass


class InlineQueryMiddleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ["inline_query"]

    def pre_process(self, query: InlineQuery, data):
        if len(query.query) == 0:
            data["not_allowed"] = True
            return

        query_params = query.query.split("_")
        if len(query_params) == 1:
            data["not_allowed"] = True
            return

        inline_prefixes = query_params[0].split()
        inline_suffix = query_params[1]

        if len(inline_prefixes) == 1:
            data["command"] = inline_prefixes[0]
        elif len(inline_prefixes) == 2:
            data["role"], data["command"] = inline_prefixes

        data["subject"] = inline_suffix
        data["not_allowed"] = False

    def post_process(self, message, data, exception=None):
        pass
