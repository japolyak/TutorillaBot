from bot.bot_token import bot
import logging
from bot.handlers import registration, localization
from bot.handlers.tutor import reply_tutor_keyboard
from bot.handlers.student import reply_student_keyboard
from bot.handlers import shared


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


if __name__ == '__main__':
    logging.info('Starting bot..')

    logging.info('Initializing handlers')

    logging.info('Starting polling')
    bot.polling(none_stop=True)
