from typing import Literal, Callable

from src.common.bot import bot
from src.common.models import SubjectDto, UserRequestDto, Role, ItemsDto

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.subject_client import SubjectClient
from src.bot.src.services.api.clients.admin_client import AdminClient
from src.bot.src.services.redis_service.redis_client import r
from src.bot.src.services.i18n.i18n import t


def get_subjects(user_id: int, role: Literal[Role.Tutor, Role.Student], locale: str):
    request = SubjectClient.get_users_subjects(user_id, role, False)

    if not request.ok:
        bot.send_message(chat_id=user_id,
                         text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                         disable_notification=True)
        return

    response_data: ItemsDto[SubjectDto] = ItemsDto[SubjectDto](**request.json())

    if not response_data.items:
        bot.send_message(chat_id=user_id, text=t(user_id, "YouHaveNoCourses", locale), disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.subjects_markup(courses=response_data.items, role=role)

    bot.send_message(chat_id=user_id, text=t(user_id, "ChooseSubject", locale),
                     disable_notification=True, reply_markup=markup)


def role_requests(user_id: int, role: Literal[Role.Student, Role.Tutor], locale: str):
    request = AdminClient.role_requests(role=role)

    if not request.ok:
        bot.send_message(chat_id=user_id,
                         text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                         disable_notification=True)
        return

    response_data: ItemsDto[UserRequestDto] = ItemsDto[UserRequestDto](**request.json())

    if not response_data.items:
        bot.send_message(chat_id=user_id, text=t(user_id, "NoRequests", locale), disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.requests_markup(response_data.items, locale)

    bot.send_message(chat_id=user_id, text=t(user_id, "AllRequests", locale), disable_notification=True, reply_markup=markup)


def send_available_subjects(user_id: int, locale: str):
    request = SubjectClient.get_users_subjects(user_id, Role.Student, True)

    if not request.ok:
        bot.send_message(chat_id=user_id,
                         text="An error occurred while retrieving your data. Please try again later. If the issue persists, contact support.",
                         disable_notification=True)
        return

    response_data: ItemsDto[SubjectDto] = ItemsDto[SubjectDto](**request.json())

    if not response_data.items:
        bot.send_message(chat_id=user_id, text=t(user_id, "NoAvailableSubjects", locale), disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.sub_course_markup(courses=response_data.items)

    bot.send_message(chat_id=user_id, text=t(user_id, "ChooseSubjectToLearn", locale),
                     disable_notification=True, reply_markup=markup)


def next_stepper(chat_id: int, text: str, func: Callable, markup=None, parse_mode: str | None = None, **kwargs) -> None:
    """
    Sends message and tracks it`s answer

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param text: The text of the message.
    :type text: :obj:`str`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :param parse_mode: Mode for parsing entities in the message text.
    :type parse_mode: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """

    msg = bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, disable_notification=True,
                           reply_markup=markup)
    bot.register_next_step_handler(message=msg, callback=func, **kwargs)


def register_next_step(chat_id: int, func: Callable, field_to_save: str | None, data: str, msg_text: str, markup=None, **kwargs) -> None:
    """
    Saves user`s cache and makes next move

    :param chat_id: The message for which we want to handle new message in the same chat.
    :type chat_id: :obj:`int`

    :param func: The callback function which next new message arrives.
    :type func: :obj:`Callable[[telebot.types.Message], None]`

    :param field_to_save: The field to save in redis_service.
    :type field_to_save: :obj:`str`

    :param data: The data to save in redis_service.
    :type data: :obj:`str`

    :param msg_text: The text of the message.
    :type msg_text: :obj:`str`

    :param markup: The reply markup of the message.

    :return: None
    """
    if field_to_save:
        r.hset(str(chat_id), field_to_save, data)

    next_stepper(chat_id, msg_text, func, markup, **kwargs)
