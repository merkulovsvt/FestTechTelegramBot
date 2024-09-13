import random
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.utils.callbacks import Task1Answer, Task3Admin, Task6Answer, Task7Answer
from bot.utils.config import task1_config, task6_config, task7_config, complete_texts, absolut_task_text, pix_task_text


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


def inline_third_task_admin_choose(chat_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Подтвердить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=True))

    builder.button(text="❌ Отклонить",
                   callback_data=Task3Admin(chat_id=chat_id,
                                            approved=False))

    return builder.as_markup()


def inline_third_task_admin_result(approved: bool):
    builder = InlineKeyboardBuilder()

    if approved:
        builder.button(text="✅ Подтверждено",
                       callback_data="inactive")
    else:
        builder.button(text="❌ Отклонено",
                       callback_data="inactive")

    return builder.as_markup()


def inline_sixth_task_phys():
    builder = InlineKeyboardBuilder()

    text = task6_config.process_text
    builder.button(text="Пощадите! Я — гуманитарий!",
                   callback_data="task6_hum")

    return text, builder.as_markup()


def inline_sixth_task_hum(answer_id: Optional[int] = None):
    builder = InlineKeyboardBuilder()

    text = """Ок, сжалимся, лови задачку от Григория Остера, её точно должен решить:
Наутро после встречи с друзьями физиками и математиками английский ученый Исаак Ньютон так ослабел, что его сила стала равна всего двум ньютонам. Сможет ли усталый ученый удержать в руках стакан с кефиром массой 200 грамм?"""

    builder.button(text="✅ Сможет" if answer_id == 1 else "Сможет",
                   callback_data=Task6Answer(answer_id=1))

    builder.button(text="❌ Не сможет" if answer_id == 2 else "Не сможет",
                   callback_data=Task6Answer(answer_id=2))

    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


def inline_seventh_task_start():
    builder = InlineKeyboardBuilder()

    builder.button(text="PIX Robotics",
                   callback_data="pix_task")

    builder.button(text="«Абсолют Страхование»",
                   callback_data="absolut_task")

    text = task7_config.process_text

    return text, builder.as_markup()


def inline_absolut_task():
    builder = InlineKeyboardBuilder()

    builder.button(text="Вернуться в меню",
                   callback_data="task7_menu")

    text = absolut_task_text

    return text, builder.as_markup()


def inline_pix_task(answer_id: Optional[int] = None):
    builder = InlineKeyboardBuilder()

    builder.button(text="❌ 1️⃣" if answer_id == 1 else "1️⃣",
                   callback_data=Task7Answer(answer_id=1))
    builder.button(text="❌ 2️⃣" if answer_id == 2 else "2️⃣",
                   callback_data=Task7Answer(answer_id=2))
    builder.button(text="✅ 3️⃣" if answer_id == 3 else "3️⃣",
                   callback_data=Task7Answer(answer_id=3))

    builder.button(text="Вернуться в меню",
                   callback_data="task7_menu")

    builder.adjust(3, 1)

    text = pix_task_text

    return text, builder.as_markup()


def inline_get_prize_start():
    builder = InlineKeyboardBuilder()

    builder.button(text="🎁 Получить приз!",
                   callback_data="get_prize")

    text = complete_texts[2]

    return text, builder.as_markup()


def inline_prize_data(prize_data: dict):
    builder = InlineKeyboardBuilder()

    builder.button(text="Сайт компании",
                   url=prize_data.get('company_url'))

    text = f"Поздравляю, ты получил {prize_data.get('name')} от {prize_data.get('company_name')}."

    return text, builder.as_markup()


def inline_lottery_start(check: Optional[bool] = None):
    builder = InlineKeyboardBuilder()
    if check:
        builder.button(text="✅ Ты участвуешь в лотерее",
                       callback_data="inactive")
    else:
        builder.button(text="🎫 Участвовать в лотерее",
                       callback_data="lottery_start")

    text = complete_texts[3]

    return text, builder.as_markup()
