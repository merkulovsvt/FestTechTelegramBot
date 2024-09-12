import asyncio

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot.keyboards.contest_boards import inline_first_task_process, inline_third_task_admin_choose, \
    inline_lottery_start, \
    inline_prize_data, inline_sixth_task_hum, inline_sixth_task_phys, inline_third_task_admin_result, \
    inline_seventh_task_start, inline_get_prize_start
from bot.utils.callbacks import Task1Answer, Task3Admin, Task6Answer
from bot.utils.config import task1_config, task2_config, task3_config, task4_config, task5_config, task6_config, \
    task7_config, complete_texts
from bot.utils.filters import MTaskFilter, CTaskFilter, GotPrize
from bot.utils.requests import change_task_type, get_task_type, update_user_activity, got_prize, get_prize, \
    participate_in_lottery, set_lottery_participation
from bot.utils.states import User

router = Router()


# Хендлер для старта первого задания
@router.message(F.text.lower().contains("начать квест"),
                MTaskFilter(""),
                StateFilter(User.menu_active, User.info_active))
async def first_task_start_handler(message: types.Message, state: FSMContext):
    await message.answer(text=task1_config.start_text)
    await state.set_state(User.quest_active)

    await change_task_type(chat_id=message.chat.id,
                           task_type="start_task1")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для условия первого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task1"))
async def first_task_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к первому заданию!")

        await message.answer(text=task1_config.process_text)

        photo = FSInputFile("bot/media/task1/pic_1.jpeg")
        text, reply_markup = inline_first_task_process(question_id=1)

        await message.answer_photo(photo=photo,
                                   reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task1")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки первого задания
@router.callback_query(~F.text.lower().contains("узнать больше про работу центра"), Task1Answer.filter(),
                       StateFilter(User.quest_active),
                       CTaskFilter("do_task1"))
async def first_task_process_handler(callback: types.CallbackQuery, callback_data: Task1Answer):
    question_id = callback_data.question_id
    answer_id = callback_data.answer_id

    if question_id == answer_id and question_id < 4:
        photo = FSInputFile(f"bot/media/task1/pic_{question_id + 1}.jpeg")

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

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для условия второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task2"))
async def second_task_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим ко второму заданию!")

        await message.answer(text=task2_config.process_text,
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task2")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки второго задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task2"))
async def second_task_process_handler(message: types.Message):
    if message.text.lower() in ("vert dider", "vertdider"):
        await message.answer(text=task2_config.end_text)

        # Старт третьего задания
        await message.answer(text=task3_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task3")

    else:
        await message.answer(text="Попробуй ещё раз, проверь опечатки")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для условия третьего задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task3"))
async def third_task_conditions_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к третьему заданию!")

        await message.answer(text=task3_config.process_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task3")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки третьего задания (фото)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task3"), F.photo)
async def third_task_photo_process_handler(message: types.Message):
    file_id = message.photo[-1].file_id

    reply_markup = inline_third_task_admin_choose(chat_id=message.chat.id)

    await message.bot.send_photo(chat_id=490082094,
                                 photo=file_id,
                                 caption=f"@{message.from_user.username}",
                                 reply_markup=reply_markup)

    await message.answer(text="Ждите проверку")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки третьего задания (не фото)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task3"), ~F.photo)
async def third_task_not_photo_process_handler(message: types.Message):
    await message.answer("Это не фото 😞")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для проверки третьего задания (только админ)
@router.callback_query(Task3Admin.filter())
async def third_task_photo_process_handler(callback: types.CallbackQuery, callback_data: Task3Admin):
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

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для условий четвертого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task4"))
async def fourth_task_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к четвертому заданию!")

        await message.answer(text=task4_config.process_text)
        await message.answer(text="И следом ещё один вопрос:\nГде был Лев Ландау во время ежовщины?")
        await message.answer(text="И самое занятное: на эти два вопроса ОДИН ответ. Впишите его ниже")

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task4")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


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

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для условий пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task5"))
async def fifth_task_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к пятому заданию!")

        await message.answer(text=task5_config.process_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task5")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки пятого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task5"))
async def fifth_task_process_handler(message: types.Message):
    if message.text.lower() == "33":
        await message.answer(text=task5_config.end_text)

        # Старт шестого задания
        await message.answer(text=task6_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task6")
    else:
        await message.answer(
            text="Кажется, нужна ещё одна попытка (мы не узнаем, если ты будешь пользоваться калькулятором)")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для условий шестого задания (физ)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task6"))
async def sixth_task_phys_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к шестому заданию!")

        photo = FSInputFile("bot/media/task6/pic_1.png")
        text, reply_markup = inline_sixth_task_phys()
        await message.answer_photo(photo=photo,
                                   caption=text,
                                   reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task6_phys")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для условия шестого задания (гум)
@router.callback_query(StateFilter(User.quest_active),
                       F.data == "task6_hum",
                       CTaskFilter("do_task6_phys") or CTaskFilter("do_task6_hum"))
async def sixth_task_hum_conditions_handler(callback: types.CallbackQuery):
    await change_task_type(chat_id=callback.message.chat.id,
                           task_type="do_task6_hum")

    text, reply_markup = inline_sixth_task_hum()

    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для обработки шестого задания (физ)
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task6_phys"))
async def sixth_task_phys_process_handler(message: types.Message):
    if message.text == "33":
        await message.answer(text=task6_config.end_text)

        # Старт седьмого задания
        await message.answer(text=task7_config.start_text)
        await change_task_type(chat_id=message.chat.id,
                               task_type="start_task7")
    else:
        await message.answer(
            text="Кажется, тебе нужна ещё одна попытка")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки шестого задания (гум)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("do_task6_hum"),
                       Task6Answer.filter())
async def sixth_task_phys_process_handler(callback: types.CallbackQuery, callback_data: Task6Answer.filter()):
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

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для условий седьмого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("start_task7"))
async def seventh_task_conditions_handler(message: types.Message):
    if message.text.lower() == "код":
        await message.answer(text="Ура, код верный! Переходим к последнему заданию!")

        text, reply_markup = inline_seventh_task_start()

        await message.answer(text=text,
                             reply_markup=reply_markup)

        await change_task_type(chat_id=message.chat.id,
                               task_type="do_task7")
    else:
        await message.answer(text="Код неверный, попробуй ещё раз!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки седьмого задания
@router.message(~F.text.lower().contains("узнать больше про работу центра"),
                StateFilter(User.quest_active),
                MTaskFilter("do_task7"))
async def seventh_task_conditions_handler(message: types.Message):
    if message.text == "33":
        await message.answer(text=task7_config.end_text)

        await message.answer(text=complete_texts[0],
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await message.answer(text=complete_texts[1],
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await change_task_type(chat_id=message.chat.id,
                               task_type="complete")

        text, reply_markup = inline_get_prize_start()

        await message.answer(text=text,
                             reply_markup=reply_markup)

    else:
        await message.answer(
            text="Кажется, тебе нужна ещё одна попытка")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки получения приза (первичное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       ~GotPrize(),
                       F.data == "get_prize")
async def get_prize_handler(callback: types.CallbackQuery):
    prize_data = await get_prize(chat_id=callback.message.chat.id)

    if prize_data:
        photo = FSInputFile(f"bot/media/logos/pic_{prize_data.get('id')}.jpeg")
        text, reply_keyboard = inline_prize_data(prize_data=prize_data)
        await callback.message.answer_photo(photo=photo,
                                            caption=text,
                                            reply_keyboard=reply_keyboard)
    else:
        await callback.message.answer(text="К сожалению, подарки кончились 😔")

    text, reply_markup = inline_lottery_start()
    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)

    await callback.message.answer(text=complete_texts[4])

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для обработки получения приза (повторное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       GotPrize(),
                       F.data == "get_prize")
async def used_get_prize_handler(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы уже получили подарок! 🎁")

    if participate_in_lottery(chat_id=callback.message.chat.id):
        await callback.message.answer(text="Вы уже участвуете в лотерее! 🎫")
        await callback.message.answer(text=complete_texts[4])
    else:
        text, reply_markup = inline_lottery_start()
        await callback.message.answer(text=text,
                                      reply_markup=reply_markup)

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для обработки лотереи (первичное)
@router.callback_query(StateFilter(User.quest_active),
                       CTaskFilter("complete"),
                       GotPrize(),
                       F.data == "lottery_start")
async def lottery_prize_handler(callback: types.CallbackQuery):
    if participate_in_lottery(chat_id=callback.message.chat.id):
        await callback.message.answer(text="Вы уже участвуете в лотерее! 🎫")
    else:
        await set_lottery_participation(chat_id=callback.message.chat.id)

    await callback.message.answer(text=complete_texts[4])

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для возвращения к заданию
@router.message(F.text.lower().contains("начать квест"),
                ~MTaskFilter(""),
                StateFilter(User.menu_active, User.info_active))
async def return_task_handler(message: types.Message, state: FSMContext):
    await state.set_state(User.quest_active)
    task_type = await get_task_type(chat_id=message.chat.id)
    if task_type == "start_task1":
        await message.answer(text=task1_config.start_text)
    elif task_type == "do_task1":
        photo = FSInputFile("bot/media/task1/pic_1.jpeg")
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
        photo = FSInputFile("bot/media/task6/pic_1.png")
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
        await message.answer(text=task7_config.process_text)
    elif task_type == "complete":
        await message.answer(text=complete_texts[0],
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        await message.answer(text=complete_texts[1],
                             parse_mode="HTML",
                             disable_web_page_preview=True)

        if got_prize(chat_id=message.chat.id):
            await message.answer(text="Вы уже получили подарок! 🎁")
        else:
            text, reply_markup = inline_get_prize_start()
            await message.answer(text=text,
                                 reply_markup=reply_markup)

        if participate_in_lottery(chat_id=message.chat.id):
            await message.answer(text="Вы уже участвуете в лотерее! 🎫")
            await message.answer(text=complete_texts[4])
        else:
            text, reply_markup = inline_lottery_start
            await message.answer(text=text,
                                 reply_markup=reply_markup)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки повторного вызова квеста изнутри (not complete)
@router.message(F.text.lower().contains("начать квест"),
                StateFilter(User.quest_active),
                ~MTaskFilter("complete"))
async def inform_quest_handler(message: types.Message):
    await message.answer(text="Вы уже проходите квест!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для обработки повторного вызова квеста изнутри (complete)
@router.message(F.text.lower().contains("начать квест"),
                StateFilter(User.quest_active),
                MTaskFilter("complete"))
async def inform_complete_quest_handler(message: types.Message):
    await message.answer(text=complete_texts[0],
                         parse_mode="HTML",
                         disable_web_page_preview=True)

    await message.answer(text=complete_texts[1],
                         parse_mode="HTML",
                         disable_web_page_preview=True)

    if got_prize(chat_id=message.chat.id):
        await message.answer(text="Вы уже получили подарок! 🎁")
    else:
        text, reply_markup = inline_get_prize_start()
        await message.answer(text=text,
                             reply_markup=reply_markup)

    if participate_in_lottery(chat_id=message.chat.id):
        await message.answer(text="Вы уже участвуете в лотерее! 🎫")
        await message.answer(text=complete_texts[4])
    else:
        text, reply_markup = inline_lottery_start
        await message.answer(text=text,
                             reply_markup=reply_markup)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для inactive inline кнопок
@router.callback_query(F.data == "inactive")
async def inactive_button_handler(callback: types.CallbackQuery):
    await callback.answer()
    await update_user_activity(chat_id=callback.message.chat.id)
