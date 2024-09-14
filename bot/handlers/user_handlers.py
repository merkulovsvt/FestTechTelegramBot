from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot.keyboards.user_boards import reply_start
from bot.utils.filters import IsAdmin
from bot.utils.requests import add_user_if_not_exists, update_user_activity, get_random_user
from bot.utils.states import User

router = Router()


# Хендлер для команды /start
@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    photo = FSInputFile("bot/media/start/start_pic.png")

    if message.chat.id in [268241744, 490082094]:
        text, reply_markup = reply_start(check=True)
    else:
        text, reply_markup = reply_start()

    await message.answer_photo(photo=photo,
                               caption=text,
                               reply_markup=reply_markup,
                               parse_mode="HTML")

    await add_user_if_not_exists(chat_id=message.chat.id,
                                 username=message.from_user.username)
    await state.set_state(User.menu_active)

    await update_user_activity(chat_id=message.chat.id)


ignore_text = ("🎉 Начать квест!", "🔍 Узнать больше про работу центра", "Рандомайзер (только для Юли)")


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

    await update_user_activity(chat_id=message.chat.id)


# Хендлер для рандомайзера
@router.message(F.text == "Рандомайзер (только для Юли)", IsAdmin())
async def randomizer_handler(message: types.Message):
    winner = await get_random_user()

    await message.answer(text="@" + winner)
