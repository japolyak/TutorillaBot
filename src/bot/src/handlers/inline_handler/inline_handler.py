from redis import Redis
from telebot.types import InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from typing import Literal, List, Optional

from common import bot, r
from src.common.models import Role, PrivateCourseInlineDto

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.private_course_client import PrivateCourseClient
from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_user_management import RedisUser


def inline_handler_guard(query: InlineQuery, command: Optional[str], role: Optional[str]):
    if not command:
        return False
    user_id = query.from_user.id

    match command:
        case "Courses":
            return RedisUser.has_role(r, user_id, Role.Tutor) if role == Role.Tutor else RedisUser.has_role(r, user_id, Role.Student)
        case "Students":
            return RedisUser.has_role(r, user_id, Role.Student)
        case "Subscribe":
            return RedisUser.has_role(r, user_id, Role.Student)
        case _:
            return False

@bot.inline_handler(func=lambda query: True)
def query_text(
        query: InlineQuery,
        redis: Redis,
        not_allowed: bool,
        command: Optional[str] = None,
        role: Optional[str] = None,
        subject: Optional[str] = None,
        *args, **kwargs
):
    if not_allowed or not subject or not inline_handler_guard(query, command, role):
        return

    user_id = query.from_user.id
    locale = redis.hget(user_id, "locale")

    match command:
        case "Courses":
            get_courses_by_role(query, subject, Role.Student, locale)
        case "Subscribe":
            subscribe_course(user_id, subject, query.id, locale)
        case "Students":
            get_courses_by_role(query, subject, Role.Student, locale)
        case _:
            return


def subscribe_course(user_id: int, subject: str, inline_query_id: str, locale: str):
    response = TutorCourseClient.course_tutors(user_id=user_id, subject_name=subject)

    if not response.is_successful():
        bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
        return

    tutor_courses = response.data.items

    if not tutor_courses:
        bot.send_message(chat_id=user_id, text=t(user_id, "NoCoursesFound", locale))
        return

    courses = [
        InlineQueryResultArticle(
            id=i.id,
            title=f"{i.subject_name} {i.price}$",
            description=f"{i.tutor_name}",
            input_message_content=InputTextMessageContent(
                message_text=t(user_id, "SubscribeCourse", locale, subject=i.subject_name,
                               tutor=i.tutor_name, price=f"{i.price}$")
            ),
            reply_markup=InlineKeyboardMarkupCreator.subscribe_course_markup(i.id, user_id, locale)
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
