from bot.api.api_models import SubjectDto, UserRequestDto
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.bot_token import bot
from bot.api.clients.subject_client import SubjectClient
from typing import Literal, Callable
from bot.api.clients.admin_client import AdminClient
from bot.redis.redis_client import r


def get_subjects(chat_id: int, role: Literal["tutor", "student"]):
    request = SubjectClient.get_users_subjects(user_id=chat_id, role=role)

    msg_text = "Choose subject"

    response_data = [SubjectDto(**subject) for subject in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=chat_id, text="You have no courses", disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.subjects_markup(courses=response_data, role=role.capitalize())

    bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)


def role_requests(user_id: int, role: str):
    request = AdminClient.role_requests(role=role)

    if not request.ok:
        bot.send_message(chat_id=user_id, text="Shit, try later", disable_notification=True)
        return

    if not request.json():
        bot.send_message(chat_id=user_id, text="No requests", disable_notification=True)
        return

    response_data: list[UserRequestDto] = [UserRequestDto(**item) for item in request.json()]
    markup = InlineKeyboardMarkupCreator.requests_markup(requests=response_data)

    bot.send_message(chat_id=user_id, text="All requests", disable_notification=True, reply_markup=markup)


def send_available_subjects(user_id: int):
    request = SubjectClient.get_available_subjects(user_id=user_id, role="student")

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


def next_stepper(chat_id: int, locale: str, text: str, func: Callable, field=None, markup=None) -> None:
    """
    Sends message and tracks it`s answer

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param locale: Users locale.
    :type locale: :obj:`str`

    :param text: The text of the message.
    :type text: :obj:`str`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :field: The field to save in redis.
    :type field: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """

    msg = bot.send_message(chat_id=chat_id, text=text, disable_notification=True, reply_markup=markup)
    bot.register_next_step_handler(message=msg, callback=func, field=field, locale=locale)


def next_registration_step(chat_id: int, func: Callable, field: str, next_field: str, data: str, locale: str, msg_text: str, markup=None) -> None:
    """
    Saves user`s cache and makes next move

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :field: The field to save in redis.
    :type field: :obj:`str`

    :param next_field: The next field to save in redis.
    :type next_field: :obj:`str`

    :param data: The data to save in redis.
    :type data: :obj:`str`

    :param locale: Users locale.
    :type locale: :obj:`str`

    :param msg_text: The text of the message.
    :type msg_text: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """
    r.hset(str(chat_id), field, data)

    next_stepper(chat_id, locale, msg_text, func, next_field, markup)
