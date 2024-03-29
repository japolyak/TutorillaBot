from telebot.types import Message
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.handlers.shared import get_subjects
from bot.handlers.message_handlers.guard.tutor_button_guard import TutorButtonGuard
from bot.exception_handler import log_exception


@bot.message_handler(func=TutorButtonGuard.office_button_guard)
def my_office(message: Message):
    chat_id = message.from_user.id
    try:
        markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
        bot.send_message(chat_id=chat_id, text="Office is here", disable_notification=True, reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, my_office, e)


@bot.message_handler(regexp="My courses")
def my_courses(message: Message):
    chat_id = message.from_user.id

    try:
        get_subjects(chat_id, "tutor")

    except Exception as e:
        log_exception(chat_id, my_courses, e)


@bot.message_handler(regexp="Add course")
def add_course(message: Message):
    chat_id = message.from_user.id

    try:
        request = SubjectClient.get_available_subjects(user_id=chat_id, role="tutor")

        if not len(request.json()):
            bot.send_message(chat_id=chat_id, text="No available subjects", disable_notification=True)
            return

        response_data = [SubjectDto(**s) for s in request.json()]

        if not len(response_data):
            bot.send_message(chat_id=chat_id, text="No available subjects", disable_notification=True)
            return

        msg_text = "Choose course to teach"

        markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

        bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, add_course, e)
