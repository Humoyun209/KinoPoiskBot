from aiogram.fsm.state import State, StatesGroup


class UserFilter(StatesGroup):
    genre_name = State()
    country = State()
    year = State()