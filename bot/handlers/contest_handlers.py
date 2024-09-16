import asyncio
import os

from aiogram import Router, types, F
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from bot.keyboards.contest_boards import inline_first_task_process, inline_third_task_admin_choose, \
    inline_lottery_start, inline_prize_data, inline_sixth_task_hum, inline_sixth_task_phys, \
    inline_third_task_admin_result, inline_seventh_task_start, inline_get_prize_start, inline_absolut_task, \
    inline_pix_task
from bot.utils.callbacks import Task1Answer, Task3Admin, Task6Answer, Task7Answer
from bot.utils.config import BASE_DIR
from bot.utils.filters import MTaskFilter, CTaskFilter, GotPrize
from bot.utils.requests import change_task_type, get_task_type, got_prize, set_prize, \
    participate_in_lottery, set_lottery_participation, get_prize
from bot.utils.states import User
from bot.utils.texts import task1_config, task2_config, task3_config, task4_config, task5_config, task6_config, \
    task7_config, complete_texts

load_dotenv()
router = Router()


# Хендлер для старта первого задания
@router.message(F.text.lower().contains("начать квест"),
                MTaskFilter(""),
                StateFilter(User.menu_active, User.info_active))
async def first_task_start_handler(message: types.Message, state: FSMContext):
    photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/start/code_sticker_example.jpeg"))

    await message.answer_photo(photo=photo,
                               caption=task1_config.start_text)
    await state.set_state(User.quest_active)

    await change_task_type(chat_id=message.chat.id,
                           task_type="start_task1")


# Хендлер для условия первого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task1"))
async def first_task_conditions_handler(message: types.Message):
    if "безграничность" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к первому заданию!")

        await message.answer(text=task1_config.process_text)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/task1/pic_1.jpeg"))
        text, reply_markup = inline_first_task_process(question_id=1)

        await message.answer_photo(photo=photo,
                                   reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task1")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки первого задания
@router.callback_query(~F.text.lower().contains("узнать больше про работу центра"), Task1Answer.filter(),
                       StateFilter(User.quest_active),
                       CTaskFilter("do_task1"))
async def callback_first_task_process_handler(callback: types.CallbackQuery, callback_data: Task1Answer):
    question_id = callback_data.question_id
    answer_id = callback_data.answer_id

    if question_id == answer_id and question_id < 4:
        photo = FSInputFile(os.path.join(BASE_DIR, f"bot/media/task1/pic_{question_id + 1}.jpeg"))

        _, reply_markup = inline_first_task_process(question_id=question_id,
                                                    correct_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        text, reply_markup = inline_first_task_process(question_id=question_id + 1)

        await asyncio.sleep(0.05)

        await callback.message.edit_media(media=types.InputMediaPhoto(media=photo),
                                          reply_markup=reply_markup)

    elif question_id == answer_id and question_id == 4:

        _, reply_markup = inline_first_task_process(question_id=question_id,
                                                    correct_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        # await callback.message.answer(text=task1_config.end_text)
        await callback.message.answer(text="Всё верно!")  # Надо ли

        await callback.message.answer(text=task2_config.start_text)
        await change_task_type(chat_id=callback.message.chat.id,
                               task_type="start_task2")

    else:
        text, reply_markup = inline_first_task_process(question_id=question_id,
                                                       wrong_answer_id=answer_id)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    await callback.answer()


# Хендлер для условия второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task2"))
async def second_task_conditions_handler(message: types.Message):
    if "скорость" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим ко второму заданию!")

        await message.answer(text=task2_config.process_text,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task2")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task2"))
async def second_task_process_handler(message: types.Message):
    if "vert" in message.text.lower() and "dider" in message.text.lower():
        await message.answer(text=task2_config.end_text)

        # Старт третьего задания
        await message.answer(text=task3_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task3")

    else:
        await message.answer(text="Попробуй ещё раз, проверь опечатки")


# Хендлер для условия третьего задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task3"))
async def third_task_conditions_handler(message: types.Message):
    if "актуальность" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к третьему заданию!")

        await message.answer(text=task3_config.process_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task3")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки третьего задания (фото)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task3"), F.photo)
async def third_task_photo_process_handler(message: types.Message):
    file_id = message.photo[-1].file_id

    reply_markup = inline_third_task_admin_choose(chat_id=message.chat.id)

    await message.bot.send_photo(chat_id=os.getenv("MODERATOR_CHAT_ID"),
                                 photo=file_id,
                                 caption=f"@{message.from_user.username}",
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
async def callback_third_task_photo_process_handler(callback: types.CallbackQuery, callback_data: Task3Admin):
    chat_id = callback_data.chat_id
    approved = callback_data.approved

    reply_markup = inline_third_task_admin_result(approved=approved)

    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    if approved:

        await callback.bot.send_message(chat_id=chat_id,
                                        text=task3_config.end_text)
        # Старт четвертого задания
        await callback.bot.send_message(chat_id=chat_id,
                                        text=task4_config.start_text)
        await change_task_type(chat_id=chat_id,
                               task_type="start_task4")
    else:
        await callback.bot.send_message(chat_id=chat_id,
                                        text="Фото не подходит, попробуйте снова!")

    await callback.answer()


# Хендлер для условий четвертого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task4"))
async def fourth_task_conditions_handler(message: types.Message):
    if "доступность" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к четвертому заданию!")

        await message.answer(text=task4_config.process_text)
        await message.answer(text="И следом ещё один вопрос:\nГде был Лев Ландау во время ежовщины?")
        await message.answer(text="И самое занятное: на эти два вопроса ОДИН ответ. Впишите его ниже")

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task4")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки четвертого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task4"))
async def fourth_task_process_handler(message: types.Message):
    if "опал" in message.text.lower():
        await message.answer(text=task4_config.end_text)

        # Старт пятого задания
        await message.answer(text=task5_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task5")
    else:
        await message.answer(text="Давай ещё одну попытку!")


# Хендлер для условий пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task5"))
async def fifth_task_conditions_handler(message: types.Message):
    if "разнообразие" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к пятому заданию!")

        await message.answer(text=task5_config.process_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task5")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для обработки пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task5"))
async def fifth_task_process_handler(message: types.Message):
    if message.text.lower() == "847":
        await message.answer(text=task5_config.end_text)

        # Старт шестого задания
        await message.answer(text=task6_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task6")
    else:
        await message.answer(
            text="Кажется, нужна ещё одна попытка (мы не узнаем, если ты будешь пользоваться калькулятором)")


# Хендлер для условий шестого задания (физ)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task6"))
async def sixth_task_phys_conditions_handler(message: types.Message):
    if "эффективность" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к шестому заданию!")

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/task6/pic_1.png"))
        text, reply_markup = inline_sixth_task_phys()
        await message.answer_photo(photo=photo,
                                   caption=text,
                                   reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task6_phys")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для условия шестого задания (гум)
@router.callback_query(StateFilter(User.quest_active),
                       F.data == "task6_hum",
                       or_f(CTaskFilter("do_task6_phys"), CTaskFilter("do_task6_hum")))
async def callback_sixth_task_hum_conditions_handler(callback: types.CallbackQuery):
    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task6_hum")

    text, reply_markup = inline_sixth_task_hum()

    await callback.message.delete()

    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)
    await callback.answer()


# Хендлер для обработки шестого задания (физ)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task6_phys"))
async def sixth_task_phys_process_handler(message: types.Message):
    if "4" in message.text.lower():
        await message.answer(text=task6_config.end_text)

        # Старт седьмого задания
        await message.answer(text=task7_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task7")
    else:
        await message.answer(
            text="Кажется, тебе нужна ещё одна попытка")


# Хендлер для обработки шестого задания (гум)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task6_hum"),
                       Task6Answer.filter())
async def callback_sixth_task_phys_process_handler(callback: types.CallbackQuery, callback_data: Task6Answer):
    answer_id = callback_data.answer_id

    text, reply_markup = inline_sixth_task_hum(answer_id=answer_id)
    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    if answer_id == 1:
        await callback.message.answer(
            text='Сможет, сможет. Сила в 2 ньютона позволяет удержать целых 204 грамма кефира. '
                 'Или такое же количество грамм рассола.')

        # Старт седьмого задания
        await callback.message.answer(text=task7_config.start_text)
        await change_task_type(chat_id=callback.message.chat.id,
                               task_type="start_task7")

    await callback.answer()


# Хендлер для условий седьмого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task7"))
async def seventh_task_conditions_handler(message: types.Message):
    if "практик" in message.text.lower() and "ориентированность" in message.text.lower():
        await message.answer(text="Ура, код верный! Переходим к последнему заданию!")

        text, reply_markup = inline_seventh_task_start()

        await message.answer(text=text,
                             reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task7")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")


# Хендлер для меню седьмого задания через inline кнопку
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task7_absolut"),
                       F.data == "task7_menu")
async def callback_absolut_seventh_task_menu_handler(callback: types.CallbackQuery):
    text, reply_markup = inline_seventh_task_start()

    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task7")

    await callback.answer()


# Хендлер для меню седьмого задания через inline кнопку
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task7_pix"),
                       F.data == "task7_menu")
async def callback_pix_seventh_task_menu_handler(callback: types.CallbackQuery):
    text, reply_markup = inline_seventh_task_start()

    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task7")

    await callback.answer()


# Хендлер для обработки седьмого задания (absolut)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task7"),
                       F.data == "absolut_task")
async def callback_seventh_task_absolut_conditions_handler(callback: types.CallbackQuery):
    text, reply_markup = inline_absolut_task()

    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task7_absolut")

    await callback.answer()


# Хендлер для обработки седьмого задания (pix)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task7"),
                       F.data == "pix_task")
async def callback_seventh_task_absolut_conditions_handler(callback: types.CallbackQuery):
    text, reply_markup = inline_pix_task()

    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task7_pix")

    await callback.answer()


# Хендлер для обработки седьмого задания (absolut)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task7_absolut"))
async def seventh_task_absolut_process_handler(message: types.Message):
    if "37.5" in message.text or "37,5" in message.text:

        await message.answer(task7_config.end_text)

        await asyncio.sleep(1)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/certificate.jpg"))
        await message.answer_photo(photo=photo,
                                   caption=complete_texts[0],
                                   parse_mode="HTML",
                                   disable_web_page_preview=True)

        await asyncio.sleep(1)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/logos/company_3.jpg"))
        await message.answer_photo(photo=photo,
                                   caption=complete_texts[1],
                                   parse_mode="HTML",
                                   disable_web_page_preview=True)

        await asyncio.sleep(1)

        text, reply_markup = inline_get_prize_start()
        await message.answer(text=text,
                             reply_markup=reply_markup,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await change_task_type(chat_id=message.chat.id,
                               task_type="complete")
    else:
        await message.answer(text="Давай пересчитаем ещё раз")


# Хендлер для обработки седьмого задания (pix)
@router.callback_query(Task7Answer.filter(),
                       StateFilter(User.quest_active),
                       CTaskFilter("do_task7_pix"))
async def callback_seventh_task_absolut_process_handler(callback: types.CallbackQuery, callback_data: Task7Answer):
    answer_id = callback_data.answer_id

    text, reply_markup = inline_pix_task(answer_id=answer_id)

    await callback.message.edit_text(text=text,
                                     reply_markup=reply_markup)

    if answer_id == 1:

        await callback.message.answer(text="Процесс увольнения займет не менее 2 недель.")

    elif answer_id == 2:

        await callback.message.answer(text="Ассемблер / Си - слишком низкоуровневые языки для данной задачи, "
                                           "а изучение множества сторонних библиотек других языков и разработка "
                                           "решения займут гораздо больше 2 недель.")

    elif answer_id == 3:

        await callback.message.answer(
            text="Программный робот RPA – это самый быстрый способ роботизации бизнес процессов, "
                 "разработка рабочего прототипа займет от 2 часов до 3 дней, и все задачи "
                 "бухгалтера поможет решить")

        await asyncio.sleep(1)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/certificate.jpg"))
        await callback.message.answer_photo(photo=photo,
                                            caption=complete_texts[0],
                                            parse_mode="HTML",
                                            disable_web_page_preview=True)

        await asyncio.sleep(1)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/logos/company_3.jpg"))
        await callback.message.answer_photo(photo=photo,
                                            caption=complete_texts[1],
                                            parse_mode="HTML",
                                            disable_web_page_preview=True)

        await asyncio.sleep(1)

        text, reply_markup = inline_get_prize_start()
        await callback.message.answer(text=text,
                                      reply_markup=reply_markup,
                                      parse_mode="HTML",
                                      disable_web_page_preview=True)

        await change_task_type(chat_id=callback.message.chat.id,
                               task_type="complete")

    await callback.answer()


# Хендлер для обработки получения приза (первичное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       ~GotPrize(),
                       F.data == "get_prize")
async def callback_get_prize_handler(callback: types.CallbackQuery):
    prize_data = await set_prize(chat_id=callback.message.chat.id)

    if prize_data:
        photo = FSInputFile(
            os.path.join(BASE_DIR, f"bot/media/partners/logos/company_{prize_data.get('company_id')}.jpg"))
        text, reply_markup = inline_prize_data(prize_data=prize_data)
        await callback.message.answer_photo(photo=photo,
                                            caption=text,
                                            reply_markup=reply_markup)
    else:
        await callback.message.answer(text="К сожалению, подарки кончились 😔")

    text, reply_markup = inline_lottery_start()
    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)

    await callback.answer()


# Хендлер для обработки получения приза (повторное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       GotPrize(),
                       F.data == "get_prize")
async def callback_used_get_prize_handler(callback: types.CallbackQuery):
    prize_data = await get_prize(chat_id=callback.message.chat.id)

    photo = FSInputFile(os.path.join(BASE_DIR, f"bot/media/partners/logos/company_{prize_data.get('company_id')}.jpg"))
    text, reply_markup = inline_prize_data(prize_data=prize_data)
    await callback.message.answer_photo(photo=photo,
                                        caption=text,
                                        reply_markup=reply_markup)

    if await participate_in_lottery(chat_id=callback.message.chat.id):
        text, reply_markup = inline_lottery_start(check=True)
        await callback.message.answer(text=text,
                                      reply_markup=reply_markup)
        await callback.message.answer(text=complete_texts[4])
    else:
        text, reply_markup = inline_lottery_start()
        await callback.message.answer(text=text,
                                      reply_markup=reply_markup)

    await callback.answer()


# Хендлер для обработки лотереи (первичное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       GotPrize(),
                       F.data == "lottery_start")
async def callback_lottery_prize_handler(callback: types.CallbackQuery):
    if not await participate_in_lottery(chat_id=callback.message.chat.id):
        await set_lottery_participation(chat_id=callback.message.chat.id)

    _, reply_markup = inline_lottery_start(check=True)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    await callback.message.answer(text=complete_texts[4])

    await callback.answer()


# Хендлер для возвращения к заданию
@router.message(F.text.lower().contains("начать квест"),
                ~MTaskFilter(""),
                StateFilter(User.menu_active, User.info_active))
async def return_task_handler(message: types.Message, state: FSMContext):
    await state.set_state(User.quest_active)
    task_type = await get_task_type(chat_id=message.chat.id)

    if task_type == "start_task1":
        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/start/code_sticker_example.jpeg"))

        await message.answer_photo(photo=photo,
                                   caption=task1_config.start_text)


    elif task_type == "do_task1":
        await message.answer(text=task1_config.process_text)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/task1/pic_1.jpeg"))
        text, reply_markup = inline_first_task_process(question_id=1)

        await message.answer_photo(photo=photo,
                                   reply_markup=reply_markup)

    elif task_type == "start_task2":
        await message.answer(text=task2_config.start_text)

    elif task_type == "do_task2":
        await message.answer(text=task2_config.process_text,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

    elif task_type == "start_task3":
        await message.answer(text=task3_config.start_text)

    elif task_type == "do_task3":
        await message.answer(text=task3_config.process_text)

    elif task_type == "start_task4":
        await message.answer(text=task4_config.start_text)

    elif task_type == "do_task4":
        await message.answer(text=task4_config.process_text)
        await message.answer(text="И следом ещё один вопрос:\nГде был Лев Ландау во время ежовщины?")
        await message.answer(text="И самое занятное: на эти два вопроса ОДИН ответ.\nВпишите его ниже")

    elif task_type == "start_task5":
        await message.answer(text=task5_config.start_text)

    elif task_type == "do_task5":
        await message.answer(text=task5_config.process_text)

    elif task_type == "start_task6":
        await message.answer(text=task6_config.start_text)

    elif task_type == "do_task6_phys":
        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/task6/pic_1.png"))
        text, reply_markup = inline_sixth_task_phys()
        await message.answer_photo(photo=photo,
                                   caption=text,
                                   reply_markup=reply_markup)
    elif task_type == "do_task6_hum":
        text, reply_markup = inline_sixth_task_hum()
        await message.answer(text=text,
                             reply_markup=reply_markup)

    elif task_type == "start_task7":
        await message.answer(text=task7_config.start_text)

    elif task_type == "do_task7":

        text, reply_markup = inline_seventh_task_start()

        await message.answer(text=text,
                             reply_markup=reply_markup)

    elif task_type in ('do_task7_absolut', 'do_task7_pix'):
        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task7")

        text, reply_markup = inline_seventh_task_start()

        await message.answer(text=text,
                             reply_markup=reply_markup)

    elif task_type == "complete":
        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/certificate.jpg"))
        await message.answer_photo(photo=photo,
                                   caption=complete_texts[0],
                                   parse_mode="HTML",
                                   disable_web_page_preview=True)

        photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/logos/company_3.jpg"))
        await message.answer_photo(photo=photo,
                                   caption=complete_texts[1],
                                   parse_mode="HTML",
                                   disable_web_page_preview=True)

        if await got_prize(chat_id=message.chat.id):

            await message.answer(text=complete_texts[2],
                                 parse_mode="HTML",
                                 disable_web_page_preview=True)

            prize_data = await get_prize(chat_id=message.chat.id)

            photo = FSInputFile(
                os.path.join(BASE_DIR, f"bot/media/partners/logos/company_{prize_data.get('company_id')}.jpg"))
            text, reply_markup = inline_prize_data(prize_data=prize_data)
            await message.answer_photo(photo=photo,
                                       caption=text,
                                       reply_markup=reply_markup)
        else:
            text, reply_markup = inline_get_prize_start()
            await message.answer(text=text,
                                 reply_markup=reply_markup,
                                 parse_mode="HTML",
                                 disable_web_page_preview=True
                                 )

        if await participate_in_lottery(chat_id=message.chat.id):
            text, reply_markup = inline_lottery_start(check=True)
            await message.answer(text=text,
                                 reply_markup=reply_markup)
            await message.answer(text=complete_texts[4])
        else:
            text, reply_markup = inline_lottery_start()
            await message.answer(text=text,
                                 reply_markup=reply_markup)


# Хендлер для обработки повторного вызова квеста изнутри (not complete)
@router.message(F.text.lower().contains("начать квест"),
                StateFilter(User.quest_active),
                ~MTaskFilter("complete"))
async def inform_quest_handler(message: types.Message):
    await message.answer(text="Вы уже проходите квест!")


# Хендлер для обработки повторного вызова квеста изнутри (complete)
@router.message(F.text.lower().contains("начать квест"),
                StateFilter(User.quest_active),
                MTaskFilter("complete"))
async def inform_complete_quest_handler(message: types.Message):
    photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/certificate.jpg"))
    await message.answer_photo(photo=photo,
                               caption=complete_texts[0],
                               parse_mode="HTML",
                               disable_web_page_preview=True)

    photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/partners/logos/company_3.jpg"))
    await message.answer_photo(photo=photo,
                               caption=complete_texts[1],
                               parse_mode="HTML",
                               disable_web_page_preview=True)

    if await got_prize(chat_id=message.chat.id):

        await message.answer(text=complete_texts[2],
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        prize_data = await get_prize(chat_id=message.chat.id)

        photo = FSInputFile(
            os.path.join(BASE_DIR, f"bot/media/partners/logos/company_{prize_data.get('company_id')}.jpg"))
        text, reply_markup = inline_prize_data(prize_data=prize_data)
        await message.answer_photo(photo=photo,
                                   caption=text,
                                   reply_markup=reply_markup)

    else:
        text, reply_markup = inline_get_prize_start()
        await message.answer(text=text,
                             reply_markup=reply_markup,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

    if await participate_in_lottery(chat_id=message.chat.id):
        text, reply_markup = inline_lottery_start(check=True)
        await message.answer(text=text,
                             reply_markup=reply_markup)
        await message.answer(text=complete_texts[4])
    else:
        text, reply_markup = inline_lottery_start()
        await message.answer(text=text,
                             reply_markup=reply_markup)


# Хендлер для inactive inline кнопок
@router.callback_query(F.data == "inactive")
async def callback_inactive_button_handler(callback: types.CallbackQuery):
    await callback.answer()
