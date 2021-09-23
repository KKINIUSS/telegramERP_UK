from aiogram.dispatcher.filters.state import StatesGroup, State

class registration(StatesGroup):
    start = State()
    fio = State()
    phone = State()
    address = State()
    passport = State()
    check = State()
