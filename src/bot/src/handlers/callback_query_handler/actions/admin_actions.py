from src.common.bot import bot
from src.common.models import UserDto

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.services.i18n.i18n import t


class AdminActions:
    @classmethod
    def __send_confirmation_message(cls, user: UserDto, role: str, locale: str):
        markup = InlineKeyboardMarkupCreator.main_menu_markup(user.id, locale)
        bot.send_message(chat_id=user.id,
                         text=t(user.id, "CongratulationsYourRequestForRoleHasBeenAccepted", locale, name=user.first_name, role=role),
                         reply_markup=markup)
