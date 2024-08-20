from telebot.types import Message
from typing import Union
from src.common.bot import bot

from src.bot.src.handlers.message_handlers.commands import command_handlers, translations


@bot.message_handler(func=lambda message: True)
def main_message_handler(message: Message, command: Union[str, None]):
    if command is None:
        return

    action = command_handlers.get(command)
    if action is None:
        return

    action(message)
