from telebot.types import Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from bot.handlers.shared import role_requests


@bot.message_handler(regexp="Admin panel")
def show_admin_panel(message: Message):
    chat_id = message.from_user.id

    try:
        markup = ReplyKeyboardMarkupCreator.admin_panel_markup()
        bot.send_message(chat_id=message.from_user.id,
                         text="Admin panel is here",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, show_admin_panel, e)


@bot.message_handler(regexp="Tutor requests")
def get_tutor_role_requests(message: Message):
    chat_id = message.from_user.id

    try:
        role_requests(user_id=chat_id, role="tutor")

    except Exception as e:
        log_exception(chat_id, get_tutor_role_requests, e)


@bot.message_handler(regexp="Student requests")
def get_student_role_requests(message: Message):
    chat_id = message.from_user.id

    try:
        role_requests(user_id=chat_id, role="student")

    except Exception as e:
        log_exception(chat_id, get_student_role_requests, e)
