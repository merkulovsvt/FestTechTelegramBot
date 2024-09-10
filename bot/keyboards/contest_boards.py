import random
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.utils.callbacks import Task1Answer, Task3Admin
from bot.utils.config import task1_config


def inline_first_task_process(question_id: int, wrong_answer_id: Optional[int] = None,
                              correct_answer_id: Optional[int] = None):
    builder = InlineKeyboardBuilder()

    text = task1_config.end_text

    button_1_text = "✅ Андрей Гейм" if correct_answer_id == 1 \
        else "❌ Андрей Гейм" if wrong_answer_id == 1 else "Андрей Гейм"

    button_2_text = "✅ Пётр Капица" if correct_answer_id == 2 \
        else "❌ Пётр Капица" if wrong_answer_id == 2 else "Пётр Капица"

    button_3_text = "✅ Дмитрий Ливанов" if correct_answer_id == 3 \
        else "❌ Дмитрий Ливанов" if wrong_answer_id == 3 else "Дмитрий Ливанов"

    button_4_text = "✅ Игорь Рыбаков" if correct_answer_id == 4 \
        else "❌ Игорь Рыбаков" if wrong_answer_id == 4 else "Игорь Рыбаков"

    button1 = InlineKeyboardButton(text=button_1_text,
                                   callback_data=Task1Answer(question_id=question_id,
                                                             answer_id=1).pack())
    button2 = InlineKeyboardButton(text=button_2_text,
                                   callback_data=Task1Answer(question_id=question_id,
                                                             answer_id=2).pack())
    button3 = InlineKeyboardButton(text=button_3_text,
                                   callback_data=Task1Answer(question_id=question_id,
                                                             answer_id=3).pack())
    button4 = InlineKeyboardButton(text=button_4_text,
                                   callback_data=Task1Answer(question_id=question_id,
                                                             answer_id=4).pack())
    buttons = [button1, button2, button3, button4]
    random.shuffle(buttons)
    builder.add(*buttons)

    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


def inline_third_task_admin(chat_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Подтвердить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=True))

    builder.button(text="❌ Отклонить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=False))

    return builder.as_markup()
