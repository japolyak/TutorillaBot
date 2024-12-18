from src.common.bot import bot
from src.common.logger import log


def send_error_message(tg_user_id, message):
    bot.send_message(chat_id=tg_user_id, text=message, parse_mode="MarkdownV2")


def send_decline_message(tg_user_id):
    bot.send_message(chat_id=tg_user_id, text='Not today')


def send_test_message(tg_user_id: int | str) -> bool:
    try:
        bot.send_message(chat_id=tg_user_id, text='Hello there')
        return True
    except Exception:
        log.error(f"Unable to send a message to Telegram user with ID: {tg_user_id}.")
        return False


def send_notification_about_new_class(tg_user_id: int, user_scheduler: str, subject_name: str, schedule_datetime: str):
    message_text = f'<b>{user_scheduler}</b> has scheduled new <b>{subject_name}</b> class at <b>{schedule_datetime}</b>'
    bot.send_message(
        chat_id=tg_user_id,
        text=message_text,
        parse_mode="HTML")
