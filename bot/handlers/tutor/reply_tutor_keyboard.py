from telebot import types
from bot.api.clients.tutor_client import TutorClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from ...api.api_models import SubjectDto
from ...enums import CallBackPrefix


@bot.message_handler(regexp="Office")
def restore_redis(message: types.Message):
    markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
    bot.send_message(chat_id=message.from_user.id, text="Office is here", reply_markup=markup)


@bot.message_handler(regexp="My courses")
def my_courses(message: types.Message):
    request = TutorClient.my_courses(user_id=message.from_user.id)

    msg_text = "Choose your course"

    response_data = [SubjectDto(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=message.from_user.id, text="You have no courses")
        return

    markup = InlineKeyboardMarkupCreator.tutor_courses_markup(courses=response_data)

    bot.send_message(chat_id=message.from_user.id, text=msg_text, reply_markup=markup)


@bot.message_handler(regexp="Add course")
def add_course(message: types.Message):
    request = TutorClient.available_subjects_tutor(user_id=message.from_user.id)

    if not len(request.json()):
        bot.send_message(chat_id=message.from_user.id, text="No available subjects")
        return

    response_data = [SubjectDto(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=message.from_user.id, text="No available subjects")
        return

    msg_text = "Choose course to teach"

    markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

    bot.send_message(chat_id=message.from_user.id, text=msg_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.startswith(CallBackPrefix.AddCourse)))
def add_course_callback(call: types.CallbackQuery):
    subject_id = int(call.data.split(" ")[1])

    request = TutorClient.add_course(user_id=call.from_user.id, subject_id=subject_id)

    if not request.ok:
        request = TutorClient.available_subjects_tutor(user_id=call.from_user.id)

        response_data = [SubjectDto(**s) for s in request.json()]

        markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)
        bot.send_message(chat_id=call.from_user.id, text="Oops, try again or try later", reply_markup=markup)
        return

    bot.send_message(chat_id=call.from_user.id, text="Course added successfully")
