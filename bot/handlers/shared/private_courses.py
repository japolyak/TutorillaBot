from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.api_models import PaginatedList, PrivateClassBaseDto
from bot.enums import CallBackPrefix
from bot.callback_query_agent import get_callback_query_data
import logging


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.CourseClasses))
def get_course_classes(call: CallbackQuery):
    try:
        private_course_id, role = get_callback_query_data(CallBackPrefix.CourseClasses, call)

        inline_message_id = call.inline_message_id

        request = PrivateCourseClient.get_classes(private_course_id=private_course_id, role=role)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
            return

        request_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

        if not len(request_data.items):
            bot.send_message(chat_id=call.from_user.id, text="You dont have classes", disable_notification=True)
            return
        logging.info(msg=f"request_data - {request_data}, private_course_id - {private_course_id}, role - {role}, inline_message_id {inline_message_id}")
        markup = InlineKeyboardMarkupCreator.course_classes_markup(request_data, private_course_id, role, inline_message_id)
        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    except Exception as e:
        logging.error(msg="Exception in get_course_classes", exc_info=e)
        error_message = f"Error Occurred\n{e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.LoadPage))
def load_page(call: CallbackQuery):
    try:
        page, private_course_id, role, inline_message_id = get_callback_query_data(CallBackPrefix.LoadPage, call)

        request = PrivateCourseClient.get_classes(private_course_id=private_course_id, role=role, page=page)

        if not request.ok:
            logging.error(msg="Bad API request in load_page")
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
            return

        rsp_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

        markup = InlineKeyboardMarkupCreator.course_classes_markup(rsp_data, private_course_id, role)

        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    except Exception as e:
        logging.error(msg="Exception in load_page", exc_info=e)
        error_message = f"Error Occurred\n{e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)
