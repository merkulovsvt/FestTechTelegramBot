from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards.info_boards import info_menu, form_filter
from bot.keyboards.user_boards import reply_start
from bot.utils.requests import set_study_name, set_study_program, set_study_contact, set_expert_place_of_work, \
    set_expert_area_of_expertise, set_expert_contact, set_expert_name, update_user_activity
from bot.utils.states import User, StudyInfo, ExpertInfo

router = Router()


# Хендлер для info меню (message)
@router.message(F.text.lower().contains("узнать больше про работу центра"))
async def info_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(User.info_active)

    text, reply_markup = info_menu()
    await message.answer(text=text,
                         reply_markup=reply_markup)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для info_study меню
@router.message(StateFilter(User.info_active),
                ~F.text.lower().contains("начать квест"))
async def callback_info_study_handler(message: types.Message):
    _, reply_markup = reply_start()
    await message.answer(text="Не понимаю тебя 😔",
                         reply_markup=reply_markup)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для info меню (callback)
@router.callback_query(F.data == "cancel_form")
async def callback_info_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(User.info_active)

    _, reply_markup = reply_start()
    await callback.message.answer(text="Подача формы отменена 😔",
                                  reply_markup=reply_markup)
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для info_study меню
@router.callback_query(F.data == "info_study", StateFilter(User.info_active))
async def callback_info_study_handler(callback: types.CallbackQuery):
    text, reply_markup = form_filter(study=True)

    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для study_form формы (Запрос ИФ)
@router.callback_query(F.data == "study_form", StateFilter(User.info_active))
async def callback_info_study_form_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StudyInfo.name)
    await callback.message.answer(text="Имя Фамилия:")
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для study_form формы (Обработка ИФ)
@router.message(StateFilter(StudyInfo.name), F.text)
async def info_study_name_handler(message: types.Message, state: FSMContext):
    await set_study_name(chat_id=message.chat.id,
                         username=message.from_user.username,
                         name=message.text)

    await state.set_state(StudyInfo.program)
    await message.answer(text="Программа:")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для study_form формы (Обработка невалидных данных для ИФ)
@router.message(StateFilter(StudyInfo.name), ~F.text)
async def incorrect_info_study_name_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для study_form формы (Обработка программы)
@router.message(StateFilter(StudyInfo.program), F.text)
async def info_study_program_handler(message: types.Message, state: FSMContext):
    await set_study_program(chat_id=message.chat.id,
                            program=message.text)

    await state.set_state(StudyInfo.contact)
    await message.answer(text="Контакты:")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для study_form формы (Обработка невалидных данных для программ)
@router.message(StateFilter(StudyInfo.program), ~F.text)
async def incorrect_info_study_program_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для study_form формы (Обработка контактов)
@router.message(StateFilter(StudyInfo.contact), F.text)
async def info_study_contacts_handler(message: types.Message, state: FSMContext):
    await set_study_contact(chat_id=message.chat.id,
                            contact=message.text)
    await message.answer(text="Спасибо, данные приняты.\nМы обязательно свяжемся с вами!")

    await state.set_state(User.info_active)
    await info_menu_handler(message, state)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для study_form формы (Обработка невалидных данных для программ)
@router.message(StateFilter(StudyInfo.contact), ~F.text)
async def incorrect_info_study_contacts_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для info_expert меню
@router.callback_query(F.data == "info_expert", StateFilter(User.info_active))
async def callback_info_expert_handler(callback: types.CallbackQuery):
    text, reply_markup = form_filter(study=False)

    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для expert_form формы
@router.callback_query(F.data == "expert_form", StateFilter(User.info_active))
async def info_expert_form_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ExpertInfo.name)
    await callback.message.answer(text="Имя Фамилия:")
    await callback.answer()

    await update_user_activity(chat_id=callback.message.chat.id)


# Хендлер для expert_form формы (Обработка ИФ)
@router.message(StateFilter(ExpertInfo.name), F.text)
async def info_expert_name_handler(message: types.Message, state: FSMContext):
    await set_expert_name(chat_id=message.chat.id,
                          username=message.from_user.username,
                          name=message.text)

    await state.set_state(ExpertInfo.area_of_expertise)
    await message.answer(text="Сфера экспертности:")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка невалидных данных для ИФ)
@router.message(StateFilter(ExpertInfo.name), ~F.text)
async def incorrect_info_expert_name_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка места сферы экспертности)
@router.message(StateFilter(ExpertInfo.area_of_expertise), F.text)
async def info_expert_area_of_expertise_handler(message: types.Message, state: FSMContext):
    await set_expert_area_of_expertise(chat_id=message.chat.id,
                                       area_of_expertise=message.text)

    await state.set_state(ExpertInfo.place_of_work)
    await message.answer(text="Место работы, регалии:")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка невалидных данных для сферы экспертности)
@router.message(StateFilter(ExpertInfo.area_of_expertise), ~F.text)
async def incorrect_info_area_of_expertise_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка места работы)
@router.message(StateFilter(ExpertInfo.place_of_work), F.text)
async def info_expert_place_of_work_handler(message: types.Message, state: FSMContext):
    await set_expert_place_of_work(chat_id=message.chat.id,
                                   place_of_work=message.text)

    await state.set_state(ExpertInfo.contact)
    await message.answer(text="Контакты:")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка невалидных данных для места работы)
@router.message(StateFilter(ExpertInfo.place_of_work), ~F.text)
async def incorrect_info_expert_place_of_work_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка контактов)
@router.message(StateFilter(ExpertInfo.contact), F.text)
async def info_expert_contacts_handler(message: types.Message, state: FSMContext):
    await set_expert_contact(chat_id=message.chat.id,
                             contact=message.text)

    await state.set_state(User.info_active)
    _, reply_markup = reply_start()
    await message.answer(text="Спасибо, данные приняты.\nМы обязательно свяжемся с вами!",
                         reply_markup=reply_markup)

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для expert_form формы (Обработка невалидных данных для программ)
@router.message(StateFilter(ExpertInfo.contact), ~F.text)
async def incorrect_info_expert_contacts_handler(message: types.Message):
    await message.answer(text="Невалидный формат данных!")

    await update_user_activity(chat_id=message.chat.id)
