from typing import Literal, List
from telebot.types import InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from bot.api.api_models import TutorCourseDto, PrivateCourseDto
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.tutor_course_client import TutorCourseClient
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.exception_handler import log_exception
from bot.decorators.message_decorator import MessageDecorator
from bot.i18n.i18n import t
from bot.enums import Role
from bot.redis.redis_client import r


def inline_handler_guard(query: InlineQuery):
    query_data = query.query.split(" ")

    if len(query_data) < 2:
        return False

    context, subject = query_data

    allowed_identities = {"Tutor", "Student", "Subscribe"}

    if context not in allowed_identities:
        return False

    allowed_subjects = {"Polish", "English", "Test"}

    if subject not in allowed_subjects:
        return False

    match context:
        case "Tutor":
            return MessageDecorator.tutor_guard(query.from_user.id)
        case "Student":
            return MessageDecorator.student_guard(query.from_user.id)
        case "Subscribe":
            return MessageDecorator.student_guard(query.from_user.id)
        case _:
            return False


@bot.inline_handler(func=inline_handler_guard)
def query_text(query: InlineQuery):
    chat_id = query.from_user.id

    context, subject = query.query.split()
    locale = r.hget(chat_id, "locale")

    match context:
        case "Tutor":
            get_courses_by_role(query, subject, Role.Tutor, locale)
        case "Student":
            get_courses_by_role(query, subject, Role.Student, locale)
        case "Subscribe":
            subscribe_course(chat_id, subject, query.id, locale)
        case _:
            return


def subscribe_course(chat_id: int, subject: str, inline_query_id: str, locale: str):
    try:
        request = TutorCourseClient.course_tutors(user_id=chat_id, subject_name=subject)

        if not request.ok:
            log_exception(chat_id, query_text, api_error=True)
            return

        response_data = [TutorCourseDto(**c) for c in request.json()]

        courses = [
            InlineQueryResultArticle(
                id=i.id,
                title=f"{i.subject.name} {i.price}$",
                description=f"{i.tutor.first_name}",
                input_message_content=InputTextMessageContent(
                    message_text=t(chat_id, "SubscribeCourse", locale, subject=i.subject.name, tutor=i.tutor.first_name, price=f"{i.price}$")
                ),
                reply_markup=InlineKeyboardMarkupCreator.subscribe_course_markup(i.id, chat_id, locale)
            ) for i in response_data
        ]

        bot.answer_inline_query(inline_query_id=inline_query_id, results=courses, cache_time=0)
    except Exception as e:
        log_exception(chat_id, subscribe_course, e)


def get_courses_by_role(query: InlineQuery, subject_name: str, role: Literal[Role.Tutor, Role.Student], locale: str):
    chat_id = query.from_user.id

    try:
        request = PrivateCourseClient.get_private_courses_by_course_name(
            user_id=chat_id,
            subject_name=subject_name,
            role=role
        )

        if not request.ok:
            log_exception(chat_id, query_text, api_error=True)
            return

        if not request.json():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "NoCoursesFound", locale), disable_notification=True)
            return

        response_data = [PrivateCourseDto(**c) for c in request.json()]

        courses = create_inline_query_courses(chat_id, role, response_data, locale)

        bot.answer_inline_query(inline_query_id=query.id, results=courses, cache_time=0)
    except Exception as e:
        log_exception(chat_id, get_courses_by_role, e)


def create_inline_query_courses(chat_id: int, role: Role, payload: List[PrivateCourseDto], locale):
    return [
        InlineQueryResultArticle(
            id=i.id,
            title=i.student.first_name if role == Role.Tutor else i.course.tutor.first_name,
            description=f"{i.course.subject.name}",
            input_message_content=InputTextMessageContent(
                message_text=t(chat_id, "SubjectAndRoleInCourse", locale,
                               subject=i.course.subject.name,
                               role=role.capitalize(),
                               name=i.student.first_name if role == Role.Tutor else i.course.tutor.first_name)
            ),
            reply_markup=InlineKeyboardMarkupCreator.private_course_markup(i.id, role, locale, chat_id)
        ) for i in payload
    ]
