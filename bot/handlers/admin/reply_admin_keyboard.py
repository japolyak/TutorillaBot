from telebot.types import CallbackQuery, Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.admin_client import AdminClient
from ...api.api_models import UserRequestDto
from ...enums import CallBackPrefix, Role


@bot.message_handler(regexp="Admin panel")
def show_admin_panel(message: Message):
    markup = ReplyKeyboardMarkupCreator.admin_panel_markup()
    bot.send_message(chat_id=message.from_user.id, text="Admin panel is here", reply_markup=markup)


@bot.message_handler(regexp="Tutor requests")
def get_tutor_role_requests(message: Message):
    role_requests(user_id=message.from_user.id, role="tutor")


@bot.message_handler(regexp="Student requests")
def get_tutor_role_requests(message: Message):
    role_requests(user_id=message.from_user.id, role="student")


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.RoleRequest))
def open_user_request(call: CallbackQuery):
    role_request_id: int = int(call.data.split(" ")[1])

    request = AdminClient.role_request(role_request_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later")
        return

    role_request: UserRequestDto = UserRequestDto(**request.json())

    role: str | None = None

    if role_request.tutor_role:
        role = Role.Tutor
    elif role_request.student_role:
        role = Role.Student

    markup = InlineKeyboardMarkupCreator.request_decision_markup(user_id=role_request.user.id, role=role)
    bot.send_message(chat_id=call.from_user.id,
                     text=f"Role\n{role_request.user.first_name} {role_request.user.last_name}"
                          f"\n{role_request.user.email}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.AcceptRole))
def accept_user_request(call: CallbackQuery):
    user_id, role = int(call.data.split(" ")[1]), call.data.split(" ")[2]

    request = AdminClient.accept_user_request(user_id=user_id, role=role)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later")
        return

    bot.send_message(chat_id=call.from_user.id, text="User request accepted")


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.DeclineRole))
def decline_user_request(call: CallbackQuery):
    user_id: int = int(call.data.split(" ")[1])

    request = AdminClient.decline_user_request(user_id)

    if not request.ok:
        bot.send_message(chat_id=call.from_user.id, text="Shit, try later")
        return

    bot.send_message(chat_id=call.from_user.id, text="User request declined")


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToUsersRequests))
def decline_user_request(call: CallbackQuery):
    role: str = call.data.split(" ")[1]
    role_requests(user_id=call.from_user.id, role=role)


def role_requests(user_id: int, role: str):
    request = AdminClient.role_requests(role=role)

    if not request.ok:
        bot.send_message(chat_id=user_id, text="Shit, try later")
        return

    if not request.json():
        bot.send_message(chat_id=user_id, text="No requests")
        return

    response_data: list[UserRequestDto] = [UserRequestDto(**item) for item in request.json()]
    markup = InlineKeyboardMarkupCreator.requests_markup(requests=response_data)

    bot.send_message(chat_id=user_id, text="All requests", reply_markup=markup)
