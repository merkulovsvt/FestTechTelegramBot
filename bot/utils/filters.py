from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from sqlalchemy import select

from bot.utils.models import async_session, User


class MTaskFilter(Filter):
    def __init__(self, task_type: str):
        self.task_type = task_type

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == message.chat.id)
            )
            existing_user = result.scalars().first()

            return existing_user.task_type == self.task_type


class CTaskFilter(Filter):
    def __init__(self, task_type: str):
        self.task_type = task_type

    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> bool:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == callback.message.chat.id)
            )
            existing_user = result.scalars().first()

            return existing_user.task_type == self.task_type
