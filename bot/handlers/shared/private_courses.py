from telebot.types import CallbackQuery
from bot.api.clients.private_courses_client import PrivateCoursesClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from ...api.api_models import PrivateClassDto
from ...enums import CallBackPrefix


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.CourseClasses))
def get_course_classes(call: CallbackQuery):
    private_course_id: int = int(call.data.split(" ")[1])
    role: str = call.data.split(" ")[2]

    request = PrivateCoursesClient.get_classes(private_course_id=private_course_id, role=role)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
        return

    response_data: PrivateClassDto = PrivateClassDto(**request.json())

    markup = InlineKeyboardMarkupCreator.course_classes_markup(response_data)
    bot.send_message(chat_id=call.from_user.id, text="Courses classes", disable_notification=True, reply_markup=markup)
