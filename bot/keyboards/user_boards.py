from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from bot.utils.config import start_text


def reply_start():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🎉 Начать квест!"))
    builder.add(KeyboardButton(text="🔍 Узнать больше про работу центра"))

    text = start_text
    builder.adjust(1, repeat=True)
    return text, builder.as_markup(resize_keyboard=True, input_field_placeholder="Нажмите на кнопку") #TODO
