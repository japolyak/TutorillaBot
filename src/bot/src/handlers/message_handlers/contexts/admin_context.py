from redis import Redis
from telebot.types import Message

from src.common.bot import bot
from src.common.models import Role

from src.bot.src.handlers.message_handlers.contexts.i_context_base import IContextBase
from src.bot.src.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from src.bot.src.handlers.shared import role_requests
from src.bot.src.services.i18n.i18n import t


class AdminContext(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message, redis: Redis):
            user_id = message.from_user.id
            is_admin = redis.hget(user_id, "is_admin")

            if is_admin == "1":
                return func(user_id, redis)

        return wrapper

    @staticmethod
    @__guard
    def show_admin_panel(user_id: int, redis: Redis):
        locale = redis.hget(user_id, "locale")
        markup = ReplyKeyboardMarkupCreator.admin_panel_markup(user_id, locale)
        bot.send_message(chat_id=user_id,
                         text=t(user_id, "AdminPanelIsHere", locale),
                         disable_notification=True,
                         reply_markup=markup)

    @staticmethod
    @__guard
    def get_tutor_role_requests(user_id: int, redis: Redis):
        locale = redis.hget(user_id, "locale")
        role_requests(user_id, Role.Tutor, locale)

    @staticmethod
    @__guard
    def get_student_role_requests(user_id: int, redis: Redis):
        locale = redis.hget(user_id, "locale")
        role_requests(user_id, Role.Student, locale)
