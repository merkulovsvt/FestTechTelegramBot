import os

from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.user_boards import reply_start, inline_send_message_menu
from bot.utils.config import BASE_DIR
from bot.utils.filters import MIsAdmin, CIsAdmin
from bot.utils.requests import get_random_user, get_all_chat_ids
from bot.utils.states import User, Admin

router = Router()


# Хендлер для команды /start
@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    photo = FSInputFile(os.path.join(BASE_DIR, "bot/media/start/start_pic.png"))
    if message.chat.id in [268241744, 490082094]:
        text, reply_markup = reply_start(check=True)
    else:
        text, reply_markup = reply_start()

    await message.answer_photo(photo=photo,
                               caption=text,
                               reply_markup=reply_markup,
                               parse_mode="HTML")

    await state.set_state(User.menu_active)


ignore_text = ("🎉 Начать квест!", "🔍 Узнать больше про работу центра",
               "🤖 Рандомайзер (AdminOnly)", "/sendMessage")


# Хендлер для неверных команд до /start
@router.message(StateFilter(None))
async def incorrect_user_pre_menu_message_handler(message: types.Message):
    text = "Не понимаю тебя, отправь /start"
    await message.answer(text=text)


# Хендлер для неверных команд после /start
@router.message(StateFilter(User.menu_active), ~F.text.in_(ignore_text))
async def incorrect_user_menu_message_handler(message: types.Message):
    text = "Чтобы взаимодействовать с ботом, нажми на кнопку!"
    _, reply_markup = reply_start()

    if message.chat.id in [268241744, 490082094]:
        _, reply_markup = reply_start(check=True)
    else:
        _, reply_markup = reply_start()

    await message.answer(text=text,
                         reply_markup=reply_markup)


# Хендлер для рандомайзера
@router.message(F.text == "🤖 Рандомайзер (AdminOnly)", MIsAdmin())
async def randomizer_handler(message: types.Message):
    winner = await get_random_user()
    await message.answer(text="@" + winner if winner else "Null user, retry")


# Хендлер для отправки сообщения
@router.message(F.text == "/sendMessage", MIsAdmin())
async def start_send_message_handler(message: types.Message, state: FSMContext):
    await message.answer(text="✍️ Введите сообщение:")

    await state.set_state(Admin.typing_message_text)


# Хендлер для отправки сообщений
@router.message(StateFilter(Admin.typing_message_text), MIsAdmin(), F.text)
async def get_message_handler(message: types.Message, state: FSMContext):
    await state.update_data(admin_message=message.text)

    text, reply_markup = inline_send_message_menu(admin_text=message.text)
    await message.answer(text=text,
                         reply_markup=reply_markup,
                         parse_mode="HTML")


# Хендлер для подтверждения отправки сообщения
@router.callback_query(F.data == 'admin_message_confirm', CIsAdmin())
async def callback_confirm_send_message_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_text = data.get('admin_message')

    await state.clear()
    await state.set_state(User.menu_active)

    if message_text:
        cnt = 0
        chat_ids = await get_all_chat_ids()
        # chat_ids = [897706487, 490082094, 268241744]
        for chat_id in chat_ids:
            try:
                await callback.bot.send_message(chat_id=chat_id,
                                                text=message_text,
                                                parse_mode="HTML")
                cnt += 1
            except:
                continue

        if cnt:
            await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"✅ Сообщение отправлено ({cnt})",
                                      callback_data="inactive")]]))

        else:
            await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отменено (ошибка)",
                                      callback_data="inactive")]]))

    else:
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменено (пустое сообщение)",
                                  callback_data="inactive")]]))

    await callback.answer()


# Хендлер для отмены отправки сообщения
@router.callback_query(F.data == 'admin_message_decline', CIsAdmin())
async def callback_decline_send_message_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменено", callback_data="inactive")]]))

    await state.set_state(User.menu_active)
    await callback.answer()


# Хендлер для редактирования сообщения для отправки
@router.callback_query(F.data == 'admin_message_edit', CIsAdmin())
async def callback_edit_send_message_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(text="♻️ Введите сообщение:")

    await callback.answer()
