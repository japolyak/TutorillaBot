from telebot.types import CallbackQuery
from bot.api.clients.private_courses_client import PrivateCoursesClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from ...api.api_models import PaginatedList, PrivateClassBaseDto
from ...enums import CallBackPrefix


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.CourseClasses))
def get_course_classes(call: CallbackQuery):
    private_course_id: int = int(call.data.split(" ")[1])
    role: str = call.data.split(" ")[2]

    request = PrivateCoursesClient.get_classes(private_course_id=private_course_id, role=role)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
        return

    request_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

    if not len(request_data.items):
        bot.send_message(chat_id=call.from_user.id, text="You dont have classes", disable_notification=True)
        return

    markup = InlineKeyboardMarkupCreator.course_classes_markup(request_data, private_course_id, role)
    bot.send_message(chat_id=call.from_user.id, text="Courses classes", disable_notification=True, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.LoadPage))
def load_page(call: CallbackQuery):
    message_id = int(call.message.message_id)

    page = int(call.data.split(" ")[1])
    private_course_id = int(call.data.split(" ")[2])
    role = call.data.split(" ")[3]

    request = PrivateCoursesClient.get_classes(private_course_id=private_course_id, role=role, page=page)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
        return

    rsp_data: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](**request.json())

    markup = InlineKeyboardMarkupCreator.course_classes_markup(rsp_data, private_course_id, role)

    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=markup)
