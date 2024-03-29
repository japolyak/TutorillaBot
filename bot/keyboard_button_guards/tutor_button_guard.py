from telebot.types import Message
from bot.redis.redis_client import r


class TutorButtonGuard:
    @staticmethod
    def office_button_guard(message: Message):
        possible_values = {"Office", "Gabinet"}

        if message.text not in possible_values:
            return False

        is_tutor = r.hget(message.from_user.id, 'is_tutor') == "1"

        return is_tutor
