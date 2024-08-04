from telebot.types import InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from typing import Literal, List

from src.common.bot_token import bot

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.api_models import Role, PrivateCourseInlineDto, TutorCourseInlineDto, ItemsDto
from src.bot.src.services.api.clients.private_course_client import PrivateCourseClient
from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.i18n.i18n import t
from src.bot.src.services.redis_service.redis_client import r


def inline_handler_guard(query: InlineQuery):
    query_data = query.query.split(" ")
    chat_id = query.from_user.id

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
            return r.hget(chat_id, "is_tutor") == "1"
        case "Student":
            return r.hget(chat_id, "is_student") == "1"
        case "Subscribe":
            return r.hget(chat_id, "is_student") == "1"
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
    request = TutorCourseClient.course_tutors(user_id=chat_id, subject_name=subject)

    if not request.ok:
        bot.send_message(chat_id=chat_id,
                         text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                         disable_notification=True)
        return

    response_data = ItemsDto[TutorCourseInlineDto](**request.json())

    if not response_data.items:
        bot.send_message(chat_id=chat_id, text=t(chat_id, "NoCoursesFound", locale), disable_notification=True)
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
        ) for i in response_data.items
    ]

    bot.answer_inline_query(inline_query_id=inline_query_id, results=courses, cache_time=0)


def get_courses_by_role(query: InlineQuery, subject_name: str, role: Literal[Role.Tutor, Role.Student], locale: str):
    chat_id = query.from_user.id

    request = PrivateCourseClient.get_private_courses_by_course_name(chat_id, subject_name, role)

    if not request.ok:
        bot.send_message(chat_id=chat_id,
                         text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                         disable_notification=True)
        return

    response_data = ItemsDto[PrivateCourseInlineDto](**request.json())

    if not response_data.items:
        bot.send_message(chat_id=chat_id, text=t(chat_id, "NoCoursesFound", locale), disable_notification=True)
        return

    courses = create_inline_query_courses(chat_id, role, response_data.items, locale)

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
