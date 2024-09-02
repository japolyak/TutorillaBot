from telebot.types import CallbackQuery
from typing import Any, List

from src.common.bot import bot

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.api.clients.private_course_client import PrivateCourseClient
from src.bot.src.services.i18n.i18n import t


class SharedActions:
    @staticmethod
    def get_course_classes(call: CallbackQuery, callback_data: List[Any], **kwargs):
        chat_id = call.from_user.id

        private_course_id, role, locale = callback_data

        inline_message_id = call.inline_message_id

        response = PrivateCourseClient.get_classes(private_course_id=private_course_id, role=role, user_id=chat_id)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))

            return

        if not response.data.items:
            bot.send_message(chat_id=chat_id, text=t(chat_id, "YouDontHaveClasses", locale))
            return

        markup = InlineKeyboardMarkupCreator.course_classes_markup(response.data, private_course_id,
                                                                   role, inline_message_id, locale, chat_id)

        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    @staticmethod
    def load_page(call: CallbackQuery, callback_data: List[Any], **kwargs):
        chat_id = call.from_user.id

        page, private_course_id, role, inline_message_id, locale = callback_data

        response = PrivateCourseClient.get_classes(private_course_id, role, chat_id,  page)

        if not response.is_successful():
            bot.send_message(chat_id=chat_id, text=t(chat_id, "RetrievingDataError", locale))
            return

        markup = InlineKeyboardMarkupCreator.course_classes_markup(response.data, private_course_id,
                                                                   role, inline_message_id, locale, chat_id)

        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)
