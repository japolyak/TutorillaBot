from redis import Redis
from telebot.states.sync import StateContext
from telebot.types import Message
from typing import Optional

from common import bot

from src.bot.src.handlers.message_handlers.commands import command_handlers


@bot.message_handler(func=lambda message: True)
def main_message_handler(message: Message, redis: Redis, state: StateContext, command: Optional[str] = None,  **kwargs):
    if command is None:
        command = state.get()
        if command is None:
            return

    action = command_handlers.get(command)
    if action is None:
        return

    action(message, redis=redis, state=state)
