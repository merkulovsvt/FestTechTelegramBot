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


def inline_send_message_menu(button_name: Optional[str] = None, button_url: Optional[str] = None):
    builder = InlineKeyboardBuilder()
    check = False

    if button_name and button_url:
        builder.button(text=button_name, url=button_url)
        check = True

    builder.button(text='✅ Подтвердить',
                   callback_data='admin_message_confirm')

    builder.button(text='❌ Отменить',
                   callback_data='admin_message_decline')

    builder.button(text='♻️ Редактировать',
                   callback_data='admin_message_edit')
    if check:
        builder.adjust(1, 2, 1)
    else:
        builder.adjust(2, 1)

    return builder.as_markup()
