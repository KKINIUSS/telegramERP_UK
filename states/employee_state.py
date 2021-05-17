from aiogram.dispatcher.filters.state import StatesGroup, State


class auth_em(StatesGroup):
    auth = State()


class employer(StatesGroup):
    work = State()
    find = State()
    list = State()

class send_message(StatesGroup):
    security = State()