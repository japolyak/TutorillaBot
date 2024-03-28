from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.enums import CallBackPrefix
from bot.handlers.tutor.shared import get_subjects
from bot.callback_query_agent import get_callback_query_data


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToChoosePrivateCourse))
def back_to_choose_subject_callback(call: CallbackQuery):
    try:
        role = get_callback_query_data(CallBackPrefix.BackToChoosePrivateCourse, call)[0]

        get_subjects(call.from_user.id, role)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToPrivateCourse))
def back_to_private_course(call: CallbackQuery):
    try:
        private_course_id, inline_message_id, role = get_callback_query_data(CallBackPrefix.BackToPrivateCourse, call)

        request = PrivateCourseClient.get_private_course(user_id=call.from_user.id, private_course_id=private_course_id)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)

        markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id=private_course_id, role=role)
        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)
