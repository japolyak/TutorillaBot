from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.exception_handler import log_exception
from typing import Any, List


def subscribe_course_callback(call: CallbackQuery, callback_data: List[Any]):
    chat_id = call.from_user.id

    try:
        course_id = callback_data[0]

        request = PrivateCourseClient.enroll_in_course(user_id=chat_id, private_course_id=course_id)

        if not request.ok:
            bot.send_message(chat_id=chat_id, text="Problem occurred", disable_notification=True,)
            return

        markup = ReplyKeyboardMarkupCreator.student_classroom_markup()
        bot.send_message(chat_id=chat_id, text="You have successfully subscribed to the course",
                         disable_notification=True, reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, subscribe_course_callback, e)


def return_to_select_callback(call: CallbackQuery, *args, **kwargs):
    chat_id = call.from_user.id

    try:
        send_available_subjects(user_id=chat_id)

    except Exception as e:
        log_exception(chat_id, return_to_select_callback, e)
