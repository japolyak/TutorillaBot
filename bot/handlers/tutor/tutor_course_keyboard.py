from telebot.types import CallbackQuery
from bot.api.clients.private_course_client import PrivateCourseClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from ...api.api_models import PrivateCourseDto
from ...enums import CallBackPrefix
from .shared import get_subjects


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToChoosePrivateCourse))
def back_to_choose_subject_callback(call: CallbackQuery):
    try:
        role = call.data.split(" ")[1]
        get_subjects(call.from_user.id, role)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToPrivateCourse))
def back_to_private_course(call: CallbackQuery):
    try:
        private_course_id: int = int(call.data.split(" ")[1])
        inline_message_id: str = call.data.split(" ")[2]

        request = PrivateCourseClient.get_private_course(user_id=call.from_user.id, private_course_id=private_course_id)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)

        markup = InlineKeyboardMarkupCreator.private_course_markup(private_course_id=private_course_id, role="tutor")
        bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)
