from redis import Redis
from telebot.types import InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from typing import Literal, List

from common import bot
from src.common.models import Role, PrivateCourseInlineDto

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.private_course_client import PrivateCourseClient
from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_client import r
from src.bot.src.services.redis_service.redis_user_management import RedisUser


def inline_handler_guard(query: InlineQuery, *args, **kwargs):
    query_data = query.query.split("_")
    chat_id = query.from_user.id

    if len(query_data) < 2:
        return False

    context, subject = query_data

    context = context.split(" ")

    #TODO - remove!
    # allowed_subjects = {"Polish", "English", "Test"}
    #
    # if subject not in allowed_subjects:
    #     return False

    print(context)
    match context[-1]:
        case "Courses":
            return RedisUser.has_role(r, chat_id, Role.Tutor) if context[0] == Role.Tutor else RedisUser.has_role(r, chat_id, Role.Student)
        case "Students":
            return RedisUser.has_role(r, chat_id, Role.Student)
        case "Subscribe":
            return RedisUser.has_role(r, chat_id, Role.Student)
        case _:
            return False

#TODO - find solution to pass redis to inline_handler_guard
@bot.inline_handler(func=inline_handler_guard)
def query_text(query: InlineQuery, redis: Redis):
    chat_id = query.from_user.id

    context, subject = query.query.split("_")
    locale = redis.hget(chat_id, "locale")

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
    response = TutorCourseClient.course_tutors(user_id=chat_id, subject_name=subject)

    if not response.is_successful():
        bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
        return

    tutor_courses = response.data.items

    if not tutor_courses:
        bot.send_message(chat_id=chat_id, text=t(chat_id, "NoCoursesFound", locale))
        return

    courses = [
        InlineQueryResultArticle(
            id=i.id,
            title=f"{i.subject_name} {i.price}$",
            description=f"{i.tutor_name}",
            input_message_content=InputTextMessageContent(
                message_text=t(chat_id, "SubscribeCourse", locale, subject=i.subject_name,
                               tutor=i.tutor_name, price=f"{i.price}$")
            ),
            reply_markup=InlineKeyboardMarkupCreator.subscribe_course_markup(i.id, chat_id, locale)
        ) for i in tutor_courses
    ]

    bot.answer_inline_query(inline_query_id=inline_query_id, results=courses, cache_time=0)


def get_courses_by_role(query: InlineQuery, subject_name: str, role: Literal[Role.Tutor, Role.Student], locale: str):
    chat_id = query.from_user.id

    response = PrivateCourseClient.get_private_courses_by_course_name(chat_id, subject_name, role)

    if not response.is_successful():
        bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
        return

    if not response.data.items:
        bot.send_message(chat_id=chat_id, text=t(chat_id, "NoCoursesFound", locale))
        return

    courses = create_inline_query_courses(chat_id, role, response.data.items, locale)

    bot.answer_inline_query(inline_query_id=query.id, results=courses, cache_time=0)


def create_inline_query_courses(chat_id: int, role: Role, payload: List[PrivateCourseInlineDto], locale):
    return [
        InlineQueryResultArticle(
            id=i.id,
            title=i.person_name,
            description=f"{i.subject_name}",
            input_message_content=InputTextMessageContent(
                message_text=t(chat_id, "SubjectAndRoleInCourse", locale,
                               subject=i.subject_name,
                               role=role.capitalize(),
                               name=i.person_name)
            ),
            reply_markup=InlineKeyboardMarkupCreator.private_course_markup(i.id, role, locale, chat_id, i.number_of_classes == 0)
        ) for i in payload
    ]
