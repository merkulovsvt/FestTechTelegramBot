from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    typing_message_text = State()


class User(StatesGroup):
    menu_active = State()
    quest_active = State()
    info_active = State()


class StudyInfo(StatesGroup):
    name = State()
    program = State()
    contact = State()


class ExpertInfo(StatesGroup):
    name = State()
    area_of_expertise = State()
    place_of_work = State()
    contact = State()
