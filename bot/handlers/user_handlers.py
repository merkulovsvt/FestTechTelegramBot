from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import FSInputFile

from bot.keyboards.user_boards import reply_start
from bot.utils.requests import add_user_if_not_exists

router = Router()


# Хендлер для команды /start
@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    photo = FSInputFile("bot/media/start/start_pic.png")

    text, reply_markup = reply_start()
    await message.answer_photo(photo=photo, caption=text, reply_markup=reply_markup)

    await add_user_if_not_exists(chat_id=message.chat.id, username=message.from_user.username)


ignore_text = ("🎉 Начать квест!", "🔍 Узнать больше про работу центра")


# Хендлер для неверных команд
@router.message(StateFilter(None), ~F.text.in_(ignore_text))
async def incorrect_user_message_handler(message: types.Message):
    text = "Не понимаю тебя, отправь /start"
    await message.answer(text=text)
