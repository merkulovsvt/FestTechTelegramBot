from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.info_boards import know_new
from bot.utils.states import User

router = Router()


@router.message(F.text.lower().contains("узнать больше про работу центра"))
async def first_task_handler(message: types.Message, state: FSMContext):
    await state.set_state(User.info_active)

    text, reply_markup = know_new()
    await message.answer(text=text, reply_markup=reply_markup)
