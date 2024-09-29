from redis import Redis
from telebot.types import Message
from typing import Optional, List

from common import bot

from src.bot.src.handlers.message_handlers.commands import command_handlers


@bot.message_handler(func=lambda message: True)
def main_message_handler(message: Message, redis: Redis, command: Optional[str] = None, **kwargs):
    if command is None:
        return

    action = command_handlers.get(command)
    if action is None:
        return

    action(message, redis)
