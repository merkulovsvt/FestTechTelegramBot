from aiogram.filters.callback_data import CallbackData


class Task1Answer(CallbackData, prefix="task_1"):
    question_id: int
    answer_id: int


class Task3Admin(CallbackData, prefix="task_3"):
    chat_id: int
    approved: bool