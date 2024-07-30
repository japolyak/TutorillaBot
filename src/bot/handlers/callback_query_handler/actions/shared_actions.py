from telebot.types import CallbackQuery
from src.bot.apiold.clients.private_course_client import PrivateCourseClient
from src.bot.bot_token import bot
from src.bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.api.models import PaginatedList, PrivateClassDto
from src.bot.exception_handler import log_exception
from typing import Any, List
from src.bot.i18n.i18n import t


class SharedActions:
    @staticmethod
    def get_course_classes(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            private_course_id, role, locale = callback_data

            inline_message_id = call.inline_message_id

            request = PrivateCourseClient.get_classes(private_course_id=private_course_id, role=role, user_id=chat_id)

            if not request.ok:
                log_exception(chat_id, SharedActions.get_course_classes)

                return

            request_data = PaginatedList[PrivateClassDto](**request.json())

            if not len(request_data.items):
                bot.send_message(chat_id=chat_id, text=t(chat_id, "YouDontHaveClasses", locale), disable_notification=True)
                return

            markup = InlineKeyboardMarkupCreator.course_classes_markup(request_data, private_course_id,
                                                                       role, inline_message_id, locale, chat_id)

            bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, SharedActions.get_course_classes, e)

    @staticmethod
    def load_page(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            page, private_course_id, role, inline_message_id, locale = callback_data

            request = PrivateCourseClient.get_classes(private_course_id, role, chat_id,  page)

            if not request.ok:
                log_exception(chat_id, SharedActions.load_page)
                return

            rsp_data = PaginatedList[PrivateClassDto](**request.json())

            markup = InlineKeyboardMarkupCreator.course_classes_markup(rsp_data, private_course_id,
                                                                       role, inline_message_id, locale, chat_id)

            bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, SharedActions.load_page, e)
