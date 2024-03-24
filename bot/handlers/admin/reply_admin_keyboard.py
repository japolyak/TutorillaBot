from telebot.types import CallbackQuery, Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.admin_client import AdminClient
from ...api.api_models import UserRequestDto, UserDto
from ...enums import CallBackPrefix, Role
from bot.redis.redis_client import r


@bot.message_handler(regexp="Admin panel")
def show_admin_panel(message: Message):
    try:
        markup = ReplyKeyboardMarkupCreator.admin_panel_markup()
        bot.send_message(chat_id=message.from_user.id,
                         text="Admin panel is here",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.message_handler(regexp="Tutor requests")
def get_tutor_role_requests(message: Message):
    try:
        role_requests(user_id=message.from_user.id, role="tutor")

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.message_handler(regexp="Student requests")
def get_tutor_role_requests(message: Message):
    try:
        role_requests(user_id=message.from_user.id, role="student")

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=message.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.RoleRequest))
def open_user_request(call: CallbackQuery):
    try:
        role_request_id: int = int(call.data.split(" ")[1])

        request = AdminClient.role_request(role_request_id)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
            return

        role_request: UserRequestDto = UserRequestDto(**request.json())

        role: Role | None = None

        if role_request.tutor_role:
            role = Role.Tutor
        elif role_request.student_role:
            role = Role.Student

        markup = InlineKeyboardMarkupCreator.request_decision_markup(user_id=role_request.user.id, role=role)
        bot.send_message(chat_id=call.from_user.id,
                         text=f"Role\n{role_request.user.first_name} {role_request.user.last_name}"
                              f"\n{role_request.user.email}",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.AcceptRole))
def accept_user_request(call: CallbackQuery):
    try:
        user_id, role = int(call.data.split(" ")[1]), call.data.split(" ")[2]

        request = AdminClient.accept_user_request(user_id=user_id, role=role)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
            return

        user: UserDto = UserDto(**request.json())

        r.hset(call.from_user.id, "is_student", int(user.is_student))
        r.hset(call.from_user.id, "is_tutor", int(user.is_tutor))
        r.hset(call.from_user.id, "is_admin", int(user.is_admin))

        bot.send_message(chat_id=call.from_user.id, text="User request accepted", disable_notification=True)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.DeclineRole))
def decline_user_request(call: CallbackQuery):
    try:
        user_id: int = int(call.data.split(" ")[1])

        request = AdminClient.decline_user_request(user_id)

        if not request.ok:
            bot.send_message(chat_id=call.from_user.id, text="Shit, try later", disable_notification=True)
            return

        bot.send_message(chat_id=call.from_user.id, text="User request declined", disable_notification=True)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToUsersRequests))
def decline_user_request(call: CallbackQuery):
    try:
        role: str = call.data.split(" ")[1]
        role_requests(user_id=call.from_user.id, role=role)

    except Exception as e:
        error_message = f"Error Occurred: {e}"
        bot.send_message(chat_id=call.from_user.id, text=error_message, disable_notification=True)


def role_requests(user_id: int, role: str):
    request = AdminClient.role_requests(role=role)

    if not request.ok:
        bot.send_message(chat_id=user_id, text="Shit, try later", disable_notification=True)
        return

    if not request.json():
        bot.send_message(chat_id=user_id, text="No requests", disable_notification=True)
        return

    response_data: list[UserRequestDto] = [UserRequestDto(**item) for item in request.json()]
    markup = InlineKeyboardMarkupCreator.requests_markup(requests=response_data)

    bot.send_message(chat_id=user_id, text="All requests", disable_notification=True, reply_markup=markup)
