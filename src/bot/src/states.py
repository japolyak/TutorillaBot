from telebot.states import State, StatesGroup


class TextbookState(StatesGroup):
    first_textbook = State()
    indeterminate = State()


class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()
    email = State()
    markup = State()
    role = State()