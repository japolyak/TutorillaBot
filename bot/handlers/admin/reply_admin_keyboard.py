from telebot.types import CallbackQuery, Message
from bot.bot_token import bot
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.api.clients.admin_client import AdminClient
from bot.api.api_models import UserRequestDto, UserDto
from bot.enums import CallBackPrefix, Role
from bot.redis.redis_client import r
from bot.callback_query_agent import get_callback_query_data
from bot.exception_handler import log_exception


@bot.message_handler(regexp="Admin panel")
def show_admin_panel(message: Message):
    chat_id = message.from_user.id

    try:
        markup = ReplyKeyboardMarkupCreator.admin_panel_markup()
        bot.send_message(chat_id=message.from_user.id,
                         text="Admin panel is here",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, "show_admin_panel", e)


@bot.message_handler(regexp="Tutor requests")
def get_tutor_role_requests(message: Message):
    chat_id = message.from_user.id

    try:
        role_requests(user_id=chat_id, role="tutor")

    except Exception as e:
        log_exception(chat_id, "get_tutor_role_requests", e)


@bot.message_handler(regexp="Student requests")
def get_tutor_role_requests(message: Message):
    chat_id = message.from_user.id

    try:
        role_requests(user_id=chat_id, role="student")

    except Exception as e:
        log_exception(chat_id, "get_tutor_role_requests", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.RoleRequest))
def open_user_request(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        role_request_id = get_callback_query_data(CallBackPrefix.RoleRequest, call)[0]

        request = AdminClient.role_request(role_request_id)

        if not request.ok:
            bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
            return

        role_request: UserRequestDto = UserRequestDto(**request.json())

        role: Role | None = None

        if role_request.tutor_role:
            role = Role.Tutor
        elif role_request.student_role:
            role = Role.Student

        markup = InlineKeyboardMarkupCreator.request_decision_markup(user_id=role_request.user.id, role=role)
        bot.send_message(chat_id=chat_id,
                         text=f"Role\n{role_request.user.first_name} {role_request.user.last_name}"
                              f"\n{role_request.user.email}",
                         disable_notification=True,
                         reply_markup=markup)

    except Exception as e:
        log_exception(chat_id, "open_user_request", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.AcceptRole))
def accept_user_request(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        user_id, role = get_callback_query_data(CallBackPrefix.AcceptRole, call)

        request = AdminClient.accept_user_request(user_id=user_id, role=role)

        if not request.ok:
            bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
            return

        user: UserDto = UserDto(**request.json())

        r.hset(chat_id, "is_student", int(user.is_student))
        r.hset(chat_id, "is_tutor", int(user.is_tutor))
        r.hset(chat_id, "is_admin", int(user.is_admin))

        bot.send_message(chat_id=chat_id, text="User request accepted", disable_notification=True)

    except Exception as e:
        log_exception(chat_id, "accept_user_request", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.DeclineRole))
def decline_user_request(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        user_id: int = get_callback_query_data(CallBackPrefix.DeclineRole, call)[0]

        request = AdminClient.decline_user_request(user_id)

        if not request.ok:
            bot.send_message(chat_id=chat_id, text="Shit, try later", disable_notification=True)
            return

        bot.send_message(chat_id=chat_id, text="User request declined", disable_notification=True)

    except Exception as e:
        log_exception(chat_id, "decline_user_request", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(CallBackPrefix.BackToUsersRequests))
def decline_user_request(call: CallbackQuery):
    chat_id = call.from_user.id

    try:
        role: str = get_callback_query_data(CallBackPrefix.BackToUsersRequests, call)[0]

        role_requests(user_id=chat_id, role=role)

    except Exception as e:
        log_exception(chat_id, "decline_user_request", e)


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
