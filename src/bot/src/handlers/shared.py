from typing import Literal, Callable, Optional

from common import bot
from src.common.models import Role

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.subject_client import SubjectClient
from src.bot.src.services.api.clients.admin_client import AdminClient
from src.bot.src.services.api.clients.tutor_course_client import TutorCourseClient
from src.bot.src.services.redis_service.redis_client import r
from src.bot.src.services.i18n.i18n import t


class Shared:
    @staticmethod
    def get_subjects(user_id: int, locale: str, role: Literal[Role.Tutor, Role.Student], query_info: str):
        response = SubjectClient.get_users_subjects(user_id, role, False)

        if not response.is_successful:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            bot.send_message(chat_id=user_id, text=t(user_id, "YouHaveNoCourses", locale))
            return

        markup = InlineKeyboardMarkupCreator.subjects_markup(subjects=response.data.items, role=role,
                                                             query_info=query_info)

        bot.send_message(chat_id=user_id, text=t(user_id, "ChooseSubject", locale), reply_markup=markup)

    @staticmethod
    def get_courses_for_panel(user_id: int, locale: str, send: bool = True, message_id: Optional[int] = None):
        response = TutorCourseClient.get_courses(user_id)

        if not response.is_successful:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            bot.send_message(chat_id=user_id, text=t(user_id, "YouHaveNoCourses", locale))
            return

        markup = InlineKeyboardMarkupCreator.subjects_panel_markup(courses=response.data.items, user_id=user_id,
                                                                   locale=locale)

        if send:
            bot.send_message(chat_id=user_id, text=t(user_id, "ChooseCourse", locale), reply_markup=markup)
            return

        if not message_id:
            return

        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=t(user_id, "ChooseCourse", locale), reply_markup=markup)

        # TODO - Do I need this?
        # hide_reply_keyboard = ReplyKeyboardRemove()
        #
        # bot.send_message(chat_id=user_id, text="...", reply_markup=hide_reply_keyboard)

    @staticmethod
    def role_requests(user_id: int, role: Literal[Role.Student, Role.Tutor], locale: str):
        response = AdminClient.role_requests(role=role)

        if not response.is_successful:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            bot.send_message(chat_id=user_id, text=t(user_id, "NoRequests", locale))
            return

        markup = InlineKeyboardMarkupCreator.requests_markup(response.data.items, locale)

        bot.send_message(chat_id=user_id, text=t(user_id, "AllRequests", locale), reply_markup=markup)

    @staticmethod
    def send_available_subjects(user_id: int, locale: str):
        response = SubjectClient.get_users_subjects(user_id, Role.Student, True)

        if not response.is_successful:
            bot.send_message(chat_id=user_id, text=t(user_id, "RetrievingDataError", locale))
            return

        if not response.data.items:
            bot.send_message(chat_id=user_id, text=t(user_id, "NoAvailableSubjects", locale))
            return

        markup = InlineKeyboardMarkupCreator.sub_course_markup(courses=response.data.items)

        bot.send_message(chat_id=user_id, text=t(user_id, "ChooseSubjectToLearn", locale), reply_markup=markup)

    @staticmethod
    def next_stepper(chat_id: int, text: str, func: Callable, markup=None, parse_mode: str | None = None,
                     **kwargs) -> None:
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

        msg = bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_markup=markup)
        bot.register_next_step_handler(message=msg, callback=func, **kwargs)

    @staticmethod
    def register_next_step(chat_id: int, func: Callable, field_to_save: str | None, data: str, msg_text: str,
                           markup=None, **kwargs) -> None:
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

        Shared.next_stepper(chat_id, msg_text, func, markup, **kwargs)
