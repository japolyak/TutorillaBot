from ...api.api_models import SubjectDto
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.bot_token import bot
from bot.api.clients.subject_client import SubjectClient


def get_tutor_subjects(chat_id: int):
    request = SubjectClient.get_classes(user_id=chat_id, role="tutor")

    msg_text = "Choose your course"

    response_data = [SubjectDto(**subject) for subject in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=chat_id, text="You have no courses", disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.tutor_courses_markup(courses=response_data)

    bot.send_message(chat_id=chat_id, text=msg_text, disable_notification=True, reply_markup=markup)
