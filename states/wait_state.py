from aiogram.dispatcher.filters.state import StatesGroup, State


class wait(StatesGroup):
    ver: State = State()
