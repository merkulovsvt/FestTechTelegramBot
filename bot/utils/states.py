from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    quest_active = State()
    info_active = State()
