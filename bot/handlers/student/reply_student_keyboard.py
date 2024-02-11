from telebot.types import Message, CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.api.clients.subject_client import SubjectClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from ...api.api_models import SubjectDto
from ..tutor.shared import get_subjects


@bot.message_handler(regexp="Classroom")
def restore_redis(message: Message):
    markup = ReplyKeyboardMarkupCreator.student_classroom_markup()

    bot.send_message(chat_id=message.from_user.id,
                     text="Your classroom is here",
                     disable_notification=True,
                     reply_markup=markup)


@bot.message_handler(regexp="My classes")
def my_courses(message: Message):
    get_subjects(message.from_user.id, "student")


@bot.message_handler(regexp="Subscribe course")
def subscribe_course(message: Message):
    send_available_subjects(user_id=message.from_user.id)


@bot.callback_query_handler(func=lambda call: (call.data.startswith("SubscribeCourse")))
def subscribe_course_callback(call: CallbackQuery):
    course_id = int(call.data.split(" ")[1])

    request = PrivateCourseClient.enroll_in_course(user_id=call.from_user.id, private_course_id=course_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Problem occurred", disable_notification=True,)
        return

    markup = ReplyKeyboardMarkupCreator.student_classroom_markup()
    bot.send_message(chat_id=call.from_user.id, text="You have successfully subscribed to the course",
                     disable_notification=True, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.startswith("ReturnToSelect")))
def return_to_select_callback(call: CallbackQuery):
    send_available_subjects(user_id=call.from_user.id)


def send_available_subjects(user_id: int):
    request = SubjectClient.get_available_subjects(user_id=user_id, role="student")
    print(request.json())

    if not len(request.json()):
        bot.send_message(chat_id=user_id, text="No available subjects", disable_notification=True)
        return

    response_data = [SubjectDto(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=user_id, text="No available subjects", disable_notification=True)
        return

    msg_text = "Choose subject to learn"

    markup = InlineKeyboardMarkupCreator.sub_course_markup(courses=response_data)

    bot.send_message(chat_id=user_id, text=msg_text, disable_notification=True, reply_markup=markup)
