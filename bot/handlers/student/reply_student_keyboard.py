from telebot import types
from bot.api.clients.student_client import StudentClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from ...api.api_models import Subject


@bot.message_handler(regexp="Classroom")
def restore_redis(message: types.Message):
    markup = ReplyKeyboardMarkupCreator.student_classroom_markup()

    bot.send_message(chat_id=message.chat.id, text="Your classroom is here", reply_markup=markup)


@bot.message_handler(regexp="My classes")
def my_courses(message: types.Message):
    request = StudentClient.my_classes(user_id=message.from_user.id)

    msg_text = "Choose your subject"

    response_data = [Subject(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=message.chat.id, text="You have no courses")
        return

    markup = InlineKeyboardMarkupCreator.student_courses_markup(courses=response_data)

    bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=markup)


@bot.message_handler(regexp="Subscribe course")
def subscribe_course(message: types.Message):
    send_available_subjects(user_id=message.from_user.id)


@bot.callback_query_handler(func=lambda call: (call.data.startswith("Subscribe course")))
def subscribe_course_callback(call: types.CallbackQuery):
    course_id = int(call.data.split(" ")[2])

    request = StudentClient.enroll_in_course(user_id=call.from_user.id, course_id=course_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Problem occurred")
        return

    markup = ReplyKeyboardMarkupCreator.student_classroom_markup()
    bot.send_message(chat_id=call.from_user.id, text="You have successfully subscribed to the course", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.startswith("Return to select")))
def return_to_select_callback(call: types.CallbackQuery):
    send_available_subjects(user_id=call.from_user.id)


def send_available_subjects(user_id: int):
    request = StudentClient.available_courses_student(user_id=user_id)

    if not len(request.json()):
        bot.send_message(chat_id=user_id, text="No available subjects")
        return

    response_data = [Subject(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=user_id, text="No available subjects")
        return

    msg_text = "Choose subject to learn"

    markup = InlineKeyboardMarkupCreator.sub_course_markup(courses=response_data)

    bot.send_message(chat_id=user_id, text=msg_text, reply_markup=markup)