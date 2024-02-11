from ...api.api_models import SubjectDto
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.bot_token import bot
from bot.api.clients.subject_client import SubjectClient
from typing import Literal


def get_subjects(chat_id: int, role: Literal["tutor", "student"]):
    request = SubjectClient.get_users_subjects(user_id=chat_id, role=role)

    msg_text = "Choose subject"

    response_data = [SubjectDto(**subject) for subject in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=chat_id, text="You have no courses", disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.subjects_markup(courses=response_data, role=role.capitalize())

    bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)
