from telebot.types import CallbackQuery
from bot.api.clients.tutor_client import TutorClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from ...api.api_models import SubjectDto, PrivateClassDto, PrivateCourseDto
from ...enums import CallBackPrefix


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.TutorCourseClasses))
def get_classes(call: CallbackQuery):
    private_course_id: int = int(call.data.split(" ")[1])

    request = TutorClient.get_classes(user_id=call.from_user.id, private_course_id=private_course_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later")
        return

    response_data: PrivateClassDto = PrivateClassDto(**request.json())

    markup = InlineKeyboardMarkupCreator.course_classes_markup(response_data)
    bot.send_message(chat_id=call.from_user.id, text="Courses classes", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == CallBackPrefix.BackToChoosePrivateCourse)
def back_to_choose_course_callback(call: CallbackQuery):
    request = TutorClient.my_courses(user_id=call.from_user.id)

    msg_text = "Choose your course"

    response_data = [SubjectDto(**subject) for subject in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=call.from_user.id, text="You have no courses")
        return

    markup = InlineKeyboardMarkupCreator.tutor_courses_markup(courses=response_data)

    bot.send_message(chat_id=call.from_user.id, text=msg_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToPrivateCourse))
def back_to_private_course(call: CallbackQuery):
    private_course_id: int = int(call.data.split(" ")[1])

    request = TutorClient.get_private_course(user_id=call.from_user.id, private_course_id=private_course_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later")

    response_data: PrivateCourseDto = PrivateCourseDto(**request.json())

    markup = InlineKeyboardMarkupCreator.tutor_student_course_markup(response_data)
    bot.send_message(chat_id=call.from_user.id,
                     text=f"Subject: {response_data.course.subject.name}\nhOther details...",
                     reply_markup=markup)
