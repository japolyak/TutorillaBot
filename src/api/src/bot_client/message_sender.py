from src.api.src.database.models import User
from src.core.config import support_nick
from src.core.bot.bot import bot
from src.core.bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.core.bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.core.logger import log

class MessageSender:
    @staticmethod
    def send_accept_role_message(user: User) -> bool:
        try:
            markup = ReplyKeyboardMarkupCreator.welcome_markup(user.id, user.locale, is_admin=user.is_admin,
                                                               is_tutor=user.is_tutor, is_student=user.is_student)
            bot.send_message(chat_id=user.id, text="Congratulations! Welcome to Tutorilla team.", reply_markup=markup)
            return True
        except Exception:
            log.error(f"Unable to send a message to Telegram user with ID: {user.id}.")
            return False

    @staticmethod
    def send_error_message(tg_user_id, message, disable_notification: bool):
        bot.send_message(chat_id=tg_user_id, text=message, parse_mode="MarkdownV2", disable_notification=disable_notification)

    @staticmethod
    def send_decline_message(tg_user_id):
        bot.send_message(chat_id=tg_user_id, text=f"Your role request was declined. Please reach support {support_nick}")

    @staticmethod
    def send_notification_about_new_class(tg_user_id: int, user_scheduler: str, subject_name: str, event_id: int):
        message_text = f'<b>{user_scheduler}</b> has scheduled new <b>{subject_name}</b> class'
        markup = InlineKeyboardMarkupCreator.new_class(event_id)
        bot.send_message(
            chat_id=tg_user_id,
            text=message_text,
            parse_mode="HTML",
            reply_markup=markup)
