from bot.redis.redis_client import r
from telebot.types import Message


class MessageDecorator:
    # TODO - rewrite all methods to use them as decorators
    @staticmethod
    def main_view_guard(chat_id):
        is_active_state = r.hget(chat_id, "is_active")

        return is_active_state == "1" or is_active_state == "0"

    @staticmethod
    def tutor_guard(chat_id):
        is_tutor = r.hget(chat_id, "is_tutor")

        return is_tutor == "1"

    @staticmethod
    def student_guard(chat_id):
        is_student = r.hget(chat_id, "is_student")

        return is_student == "1"

    @staticmethod
    def admin_guard(chat_id):
        is_student = r.hget(chat_id, "is_admin")

        return is_student == "1"

    @classmethod
    def is_user_registered(cls, func):
        def wrapper(message: Message):
            is_active_state = r.hget(message.from_user.id, "is_active")
            if is_active_state == "1" or is_active_state == "0":
                return func(message)
            return None

        return wrapper

    @classmethod
    def is_tutor(cls, func):
        def wrapper(message: Message):
            is_tutor = r.hget(message.from_user.id, "is_tutor")
            if is_tutor == "1":
                return func(message)

            return None

        return wrapper

    @classmethod
    def is_student(cls, func):
        def wrapper(message: Message):
            is_tutor = r.hget(message.from_user.id, "is_student")
            if is_tutor == "1":
                return func(message)

            return None

        return wrapper

    @classmethod
    def is_admin(cls, func):
        def wrapper(message: Message):
            is_admin = r.hget(message.from_user.id, "is_admin")
            if is_admin == "1":
                return func(message)

            return None

        return wrapper
