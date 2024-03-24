from telebot.types import Message, CallbackQuery
from bot.api.clients.tutor_course_client import TutorCourseClient
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.api.api_models import SubjectDto
from bot.enums import CallBackPrefix
from bot.handlers.tutor.shared import get_subjects
from bot.callback_query_agent import get_callback_query_data


@bot.message_handler(regexp="Office")
def restore_redis(message: Message):
    try:
        markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
        bot.send_message(chat_id=message.from_user.id, text="Office is here", disable_notification=True, reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.message_handler(regexp="My courses")
def my_courses(message: Message):
    try:
        get_subjects(message.from_user.id, "tutor")

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.message_handler(regexp="Add course")
def add_course(message: Message):
    try:
        request = SubjectClient.get_available_subjects(user_id=message.from_user.id, role="tutor")

        if not len(request.json()):
            bot.send_message(chat_id=message.from_user.id, text="No available subjects", disable_notification=True)
            return

        response_data = [SubjectDto(**s) for s in request.json()]

        if not len(response_data):
            bot.send_message(chat_id=message.from_user.id, text="No available subjects", disable_notification=True)
            return

        msg_text = "Choose course to teach"

        markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

        bot.send_message(chat_id=message.from_user.id, text=msg_text, disable_notification=True, reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: (call.data.startswith(CallBackPrefix.AddCourse)))
def add_course_callback(call: CallbackQuery):
    try:
        subject_id: int = get_callback_query_data(CallBackPrefix.AddCourse, call)[0]

        request = TutorCourseClient.add_course(user_id=call.from_user.id, subject_id=subject_id)

        if not request.ok:
            request = SubjectClient.get_available_subjects(user_id=call.from_user.id, role="tutor")

            response_data = [SubjectDto(**s) for s in request.json()]

            markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)
            bot.send_message(chat_id=call.from_user.id, text="Oops, try again or try later",
                             disable_notification=True, reply_markup=markup)
            return

        bot.send_message(chat_id=call.from_user.id, text="Course added successfully", disable_notification=True)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)
