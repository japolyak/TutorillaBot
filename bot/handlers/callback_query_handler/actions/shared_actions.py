from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.api_models import PaginatedList, PrivateClassBaseDto
from bot.exception_handler import log_exception
from typing import Any, List


class SharedActions:
    @staticmethod
    def get_course_classes(call: CallbackQuery, callback_data: List[Any]):
        chat_id = call.from_user.id

        try:
            private_course_id, role, locale = callback_data

            inline_message_id = call.inline_message_id

            request = PrivateCourseClient.get_classes(private_course_id=private_course_id, role=role)

            if not request.ok:
                log_exception(chat_id, SharedActions.get_course_classes)

                return

            request_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

            if not len(request_data.items):
                bot.send_message(chat_id=chat_id, text="You dont have classes", disable_notification=True)
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

            request = PrivateCourseClient.get_classes(private_course_id, role, page)

            if not request.ok:
                log_exception(chat_id, SharedActions.load_page)
                return

            rsp_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

            markup = InlineKeyboardMarkupCreator.course_classes_markup(rsp_data, private_course_id,
                                                                       role, inline_message_id, locale, chat_id)

            bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, SharedActions.load_page, e)
