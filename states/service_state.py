from aiogram.dispatcher.filters.state import StatesGroup, State


class choice_service(StatesGroup):
    choice: State = State()


class add_guest(StatesGroup):
    get_name: State = State()
    get_phone: State = State()
