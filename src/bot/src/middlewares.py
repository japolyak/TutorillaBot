from redis import Redis
from telebot.handler_backends import BaseMiddleware
from telebot.types import Message
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