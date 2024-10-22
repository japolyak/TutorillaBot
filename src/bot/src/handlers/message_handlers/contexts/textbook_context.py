from telebot.types import Message
from telebot.states.sync import StateContext

from src.common.bot import bot

from src.bot.src.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from src.bot.src.states import TextbookState


class TextbookContext:
    @staticmethod
    def first_textbook(message: Message, state: StateContext, *args, **kwargs):
        textbooks = [message.text]
        user_id = message.from_user.id

        state.add_data(textbooks=textbooks)
        state.set(TextbookState.indeterminate)

        locale = "en-US" # TODO - remove
        markup = InlineKeyboardMarkupCreator.new_textbooks_markup(user_id, locale)

        bot.send_message(chat_id=user_id, text=f"Added textbook - {message.text}", reply_markup=markup)
