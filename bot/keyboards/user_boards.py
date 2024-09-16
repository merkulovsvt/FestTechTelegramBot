from typing import Optional

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.utils.texts import start_text


def reply_start(check: Optional[bool] = None):
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🎉 Начать квест!"))
    builder.add(KeyboardButton(text="🔍 Узнать больше про работу центра"))
    if check:
        builder.add(KeyboardButton(text="🤖 Рандомайзер (AdminOnly)"))

    text = start_text
    builder.adjust(1, repeat=True)
    return text, builder.as_markup(resize_keyboard=True,
                                   input_field_placeholder="Нажмите на кнопку")


def inline_send_message_menu(admin_text: str):
    builder = InlineKeyboardBuilder()

    text = "Сообщение:\n\n" + admin_text

    builder.button(text='✅ Подтвердить',
                   callback_data='admin_message_confirm')

    builder.button(text='❌ Отменить',
                   callback_data='admin_message_decline')

    builder.button(text='♻️ Редактировать',
                   callback_data='admin_message_edit')

    builder.adjust(2, 1)
    return text, builder.as_markup()
