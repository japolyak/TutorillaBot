from bot.redis.redis_client import r


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
        is_admin = r.hget(chat_id, "is_admin")

        return is_admin == "1"
