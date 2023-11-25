from bot.bot_token import bot
import logging


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


if __name__ == '__main__':
    logging.info('Starting bot..')

    logging.info('Starting polling')
    bot.polling(none_stop=True)
