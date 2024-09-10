from aiogram.utils.keyboard import InlineKeyboardBuilder


def know_new():
    builder = InlineKeyboardBuilder()

    builder.button(text="📚 Хочу учиться", callback_data='first')
    builder.button(text="🧠 Хочу стать экспертом Центра", callback_data='seconf')
    builder.button(text="🔍 Ссылка на проект", url='https://mipt.online/')

    text = "Нажмите на кнопку"

    builder.adjust(1, 1, 1)
    return text, builder.as_markup()
