from telebot.types import Message

from src.common.bot_token import bot

from src.bot.src.handlers.message_handlers.commands import command_handlers, translations


@bot.message_handler(func=lambda message: True)
def main_message_handler(message: Message):
    for _, commands in translations.items():
        command_name = commands.get(message.text)
        if command_name:
            action = command_handlers.get(command_name)
            if action:
                action(message)
                return
