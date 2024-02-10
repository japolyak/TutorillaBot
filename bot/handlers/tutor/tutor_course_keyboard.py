from telebot.types import CallbackQuery
from bot.api.clients.tutor_client import TutorClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from ...api.api_models import PrivateCourseDto
from ...enums import CallBackPrefix
from .shared import get_tutor_subjects


@bot.callback_query_handler(func=lambda call: call.data == CallBackPrefix.BackToChoosePrivateCourse)
def back_to_choose_course_callback(call: CallbackQuery):
    get_tutor_subjects(call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToPrivateCourse))
def back_to_private_course(call: CallbackQuery):
    private_course_id: int = int(call.data.split(" ")[1])
    inline_message_id: str = call.data.split(" ")[2]

    request = TutorClient.get_private_course(user_id=call.from_user.id, private_course_id=private_course_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)

    response_data: PrivateCourseDto = PrivateCourseDto(**request.json())

    markup = InlineKeyboardMarkupCreator.tutor_student_course_markup(response_data, "tutor")
    bot.edit_message_reply_markup(inline_message_id=inline_message_id, reply_markup=markup)
