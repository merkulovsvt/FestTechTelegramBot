import asyncio

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot.keyboards.contest_boards import first_task_process, third_task_admin
from bot.utils.callbacks import Task1Answer, Task3Admin
from bot.utils.config import task1_config, task2_config, task3_config, task4_config, task5_config, task6_config
from bot.utils.filters import MTaskFilter, CTaskFilter
from bot.utils.requests import change_task_type
from bot.utils.states import User

router = Router()


# Хендлер для старта первого задания
@router.message(F.text.lower().contains("начать квест!"),
                MTaskFilter(""))
async def first_task_start_handler(message: types.Message, state: FSMContext):
    await message.answer(text=task1_config.start_text)
    await state.set_state(User.quest_active)

    await change_task_type(chat_id=message.chat.id, task_type="start_task1")


# Хендлер для условия первого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task1")
                )
async def first_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к первому заданию!")

        await message.answer(text=task1_config.process_text)

        photo = FSInputFile("bot/media/task1/pic_1.jpg")
        text, reply_markup = first_task_process(question_id=1)

        await message.answer_photo(photo=photo,
                                   reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id, task_type="do_task1")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки первого задания
@router.callback_query(~F.text.lower().contains("узнать больше про работу центра"), Task1Answer.filter(),
                       StateFilter(User.quest_active),
                       CTaskFilter("do_task1"))
async def first_task_process_handler(callback: types.CallbackQuery, state: FSMContext, callback_data: Task1Answer):
    question_id = callback_data.question_id
    answer_id = callback_data.answer_id

    if question_id == answer_id and question_id < 4:
        photo = FSInputFile(f"bot/media/task1/pic_{question_id + 1}.jpg")

        _, reply_markup = first_task_process(question_id=question_id,
                                             correct_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        text, reply_markup = first_task_process(question_id=question_id + 1)

        await asyncio.sleep(0.05)

        await callback.message.edit_media(media=types.InputMediaPhoto(media=photo),
                                          reply_markup=reply_markup)

    elif question_id == answer_id and question_id == 4:

        _, reply_markup = first_task_process(question_id=question_id,
                                             correct_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        # await callback.message.answer(text=task1_config.end_text)
        await callback.message.answer(text="Всё верно!")  # Надо ли

        await callback.message.answer(text=task2_config.start_text)
        await change_task_type(chat_id=callback.message.chat.id, task_type="start_task2")

    else:
        text, reply_markup = first_task_process(question_id=question_id,
                                                wrong_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)
    await callback.answer()


# Хендлер для условия второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task2"))
async def second_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим ко второму заданию!")

        await message.answer(text=task2_config.process_text,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await change_task_type(chat_id=message.chat.id, task_type="do_task2")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task2"))
async def second_task_process_handler(message: types.Message, state: FSMContext):
    if message.text.lower() in ("vert dider", "vertdider"):
        await message.answer(text=task2_config.end_text)

        # Старт третьего задания
        await message.answer(text=task3_config.start_text)
        await change_task_type(chat_id=message.chat.id, task_type="start_task3")

    else:
        await message.answer(text="Попробуй ещё раз, проверь опечатки")


# Хендлер для условия третьего задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task3"))
async def third_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к третьему заданию!")

        await message.answer(text=task3_config.process_text)
        await change_task_type(chat_id=message.chat.id, task_type="do_task3")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки третьего задания (фото)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task3"), F.photo)
async def third_task_photo_process_handler(message: types.Message):
    file_id = message.photo[-1].file_id

    reply_markup = third_task_admin(chat_id=message.chat.id)

    await message.bot.send_photo(chat_id=490082094,
                                 photo=file_id,
                                 caption=f"{message.from_user.username}",
                                 reply_markup=reply_markup)

    await message.answer(text="Ждите проверку")


# Хендлер для обработки третьего задания (не фото)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task3"), ~F.photo)
async def third_task_not_photo_process_handler(message: types.Message):
    await message.answer("Это не фото 😞")


# Хендлер для проверки третьего задания (только админ)
@router.callback_query(Task3Admin.filter())
async def third_task_photo_process_handler(callback: types.CallbackQuery, callback_data: Task3Admin):
    chat_id = callback_data.chat_id
    approved = callback_data.approved

    if approved:
        await callback.bot.send_message(chat_id=chat_id, text=task3_config.end_text)

        await change_task_type(chat_id=chat_id, task_type="start_task4")
        # Старт четвертого задания
        await callback.bot.send_message(chat_id=chat_id, text=task4_config.start_text)
    else:
        await callback.bot.send_message(chat_id=chat_id, text="Фото не подходит, попробуйте снова!")

    await callback.answer()


# Хендлер для условий четвертого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task4"))
async def fourth_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text == "код":
        await message.answer(text="Ура, код верный! Переходим к четвертому заданию!")

        await message.answer(text=task4_config.process_text)
        await message.answer(text="""
        И следом ещё один вопрос:
        Где был Лев Ландау во время ежовщины?""")
        await message.answer(text="И самое занятное: на эти два вопроса ОДИН ответ. Впишите его ниже")
        await change_task_type(chat_id=message.chat.id, task_type="do_task4")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки четвертого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task4"))
async def fourth_task_process_handler(message: types.Message, state: FSMContext):
    if "опал" in message.text.lower():
        await message.answer(text=task4_config.end_text)

        # Старт пятого задания
        await message.answer(text=task5_config.start_text)
        await change_task_type(chat_id=message.chat.id, task_type="start_task5")
    else:
        await message.answer(text="Давай ещё одну попытку!")


# Хендлер для условий пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task5"))
async def fifth_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к четвертому заданию!")

        await message.answer(text=task5_config.process_text)
        await change_task_type(chat_id=message.chat.id, task_type="do_task5")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task5"))
async def fifth_task_process_handler(message: types.Message, state: FSMContext):
    if message.text == 33:
        await message.answer(text=task5_config.end_text)

        # Старт шестого задания
        await message.answer(text=task6_config.start_text)
        await change_task_type(chat_id=message.chat.id, task_type="start_task6")
    else:
        await message.answer(
            text="Кажется, нужна ещё одна попытка (мы не узнаем, если ты будешь пользоваться калькулятором)")


# Хендлер для условий шестого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task6"))
async def fifth_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к четвертому заданию!")

        await message.answer(text=task6_config.process_text)
        await change_task_type(chat_id=message.chat.id, task_type="do_task6")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")
