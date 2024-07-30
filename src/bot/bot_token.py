import telebot
from src.bot.config import token


bot = telebot.TeleBot(token, threaded=False)
