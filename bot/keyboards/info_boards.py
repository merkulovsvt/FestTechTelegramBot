from aiogram.utils.keyboard import InlineKeyboardBuilder


def info_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="📚 Хочу учиться", callback_data='info_study')
    builder.button(text="🧠 Хочу стать экспертом Центра", callback_data='info_expert')
    builder.button(text="🔍 Ссылка на проект", url='https://mipt.online/')

    text = "Нажмите на кнопку (поменять)"

    builder.adjust(1, 1, 1)
    return text, builder.as_markup()


def form_filter(study: bool):
    if study:
        text = ("Расскажите о себе и мы свяжемся с вами(поменяю)\n- Имя Фамилия\n"
                "- Направление обучения\n- Предпочтительный способ связи")
    else:
        text = ("Расскажите о себе и мы свяжемся с вами(поменяю)\n- Имя Фамилия\n"
                "- Сфера экспертности\n- Место работы, регалии\n- Предпочтительный способ связи")

    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="study_form" if study else "expert_form")
    builder.button(text="Отмена", callback_data='cancel_form')

    return text, builder.as_markup()
