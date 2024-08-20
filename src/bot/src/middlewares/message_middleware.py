from telebot.handler_backends import BaseMiddleware
from telebot.types import Message
from telebot.util import update_types


class MessageMiddleware(BaseMiddleware):
    def __init__(self):
        self.update_types = update_types

    def pre_process(self, message: Message, data):
        if message.text.startswith("/"):
            return



    def post_process(self, message, data, exception=None):
        pass