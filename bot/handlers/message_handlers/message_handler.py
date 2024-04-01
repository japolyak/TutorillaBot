from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.message_handlers.commands import command_handlers, translations


@bot.message_handler(func=lambda message: True)
def main_message_handler(message: Message):
    for _, j in translations.items():
        if message.text in j.keys():
            action = command_handlers[j[message.text]]
            action(message)

            return
