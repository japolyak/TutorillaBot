from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception


@bot.message_handler(regexp="Classroom")
def open_classroom(message: Message):
    chat_id = message.from_user.id

    try:
        markup = ReplyKeyboardMarkupCreator.student_classroom_markup()

        bot.send_message(chat_id=chat_id,
                         text="Your classroom is here",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, open_classroom, e)


@bot.message_handler(regexp="My classes")
def my_courses(message: Message):
    chat_id = message.from_user.id

    try:
        get_subjects(chat_id, "student")

    except Exception as e:
        log_exception(chat_id, my_courses, e)


@bot.message_handler(regexp="Subscribe course")
def subscribe_course(message: Message):
    chat_id = message.from_user.id

    try:
        send_available_subjects(user_id=chat_id)

    except Exception as e:
        log_exception(chat_id, subscribe_course, e)
