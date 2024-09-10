from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import Task1Answer, Task3Admin
from bot.utils.config import task1_config


def first_task_process(question_id: int, wrong_answer_id: Optional[int] = None,
                       correct_answer_id: Optional[int] = None):
    builder = InlineKeyboardBuilder()

    text = task1_config.end_text

    button_1_text = "✅ Гейм" if correct_answer_id == 1 else "❌ Гейм" if wrong_answer_id == 1 else "Гейм"
    button_2_text = "✅ Капица" if correct_answer_id == 2 else "❌ Капица" if wrong_answer_id == 2 else "Капица"
    button_3_text = "✅ Ливанов" if correct_answer_id == 3 else "❌ Ливанов" if wrong_answer_id == 3 else "Ливанов"
    button_4_text = "✅ Рыбаков" if correct_answer_id == 4 else "❌ Рыбаков" if wrong_answer_id == 4 else "Рыбаков"

    builder.button(text=button_2_text,
                   callback_data=Task1Answer(question_id=question_id,
                                             answer_id=2))

    builder.button(text=button_1_text,
                   callback_data=Task1Answer(question_id=question_id,
                                             answer_id=1))

    builder.button(text=button_4_text,
                   callback_data=Task1Answer(question_id=question_id,
                                             answer_id=4))

    builder.button(text=button_3_text,
                   callback_data=Task1Answer(question_id=question_id,
                                             answer_id=3))

    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


def third_task_admin(chat_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Подтвердить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=True))

    builder.button(text="❌ Отклонить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=False))

    return builder.as_markup()
