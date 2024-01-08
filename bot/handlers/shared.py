from telebot.types import InputTextMessageContent, Message, InlineQuery, InlineQueryResultArticle
from bot.api.api_models import TutorCourseDto, PrivateCourseDto
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.student_client import StudentClient
from bot.api.clients.tutor_client import TutorClient


@bot.message_handler(regexp="Main menu")
def main_menu(message: Message):
    markup = ReplyKeyboardMarkupCreator.main_menu_markup(message.from_user.id)
    bot.send_message(chat_id=message.from_user.id, text="Main menu", reply_markup=markup)


repeated_inline_query_result = [InlineQueryResultArticle(id="1", title="Bad request",
                                                         input_message_content=InputTextMessageContent(
                                                             message_text="Bad request"))]


@bot.inline_handler(func=lambda query: query.query)
def query_text(query: InlineQuery):
    subject = query.query.split(" ")

    if len(subject) and query.query.startswith("Tutor"):
        request = TutorClient.private_courses(user_id=query.from_user.id, subject_name=subject[1])

        if not request.ok:
            bot.answer_inline_query(query.id, repeated_inline_query_result)
            return

        if not request.json():
            bot.answer_inline_query(query.id, repeated_inline_query_result)
            return

        response_data = [PrivateCourseDto(**c) for c in request.json()]

        courses = [
            InlineQueryResultArticle(
                id=i.id,
                title=f"{i.student.first_name} {i.student.last_name}",
                description=f"{i.course.subject.name}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Subject: {i.course.subject.name}\nhOther details..."
                ),
                reply_markup=InlineKeyboardMarkupCreator.tutor_student_course_markup(i)
            ) for i in response_data
        ]

        bot.answer_inline_query(inline_query_id=query.id, results=courses, cache_time=0)
        return

    if len(subject) and query.query.startswith("Student"):
        request = StudentClient.private_courses(user_id=query.from_user.id, subject_name=subject[1])

        if not request.ok:
            bot.answer_inline_query(query.id, repeated_inline_query_result)

            return

        response_data = [PrivateCourseDto(**c) for c in request.json()]

        courses = [
            InlineQueryResultArticle(
                id=i.id,
                title=f"{i.course.subject.name}",
                description=f"{i.course.tutor.first_name} {i.course.tutor.last_name}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Subject: {i.course.subject.name}\nOther details..."
                )
            ) for i in response_data
        ]

        bot.answer_inline_query(inline_query_id=query.id, results=courses, cache_time=0)
        return

    if len(subject) and query.query.startswith("Subscribe"):
        request = StudentClient.course_tutors(user_id=query.from_user.id, subject_name=subject[1])
        if not request.ok:
            bot.answer_inline_query(query.id, repeated_inline_query_result)
            return

        response_data = [TutorCourseDto(**c) for c in request.json()]

        courses = [
            InlineQueryResultArticle(
                id=i.id,
                title=f"{i.subject.name}",
                description=f"{i.tutor.first_name} {i.tutor.last_name}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Subject: {i.subject.name}\n With {i.tutor.first_name} {i.tutor.last_name}"
                ),
                reply_markup=InlineKeyboardMarkupCreator.subscribe_course_markup(i.id)
            ) for i in response_data
        ]

        bot.answer_inline_query(inline_query_id=query.id, results=courses, cache_time=0)
        return
