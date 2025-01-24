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
                select(User).where(User.chat_id == message.chat.id))
            return result.scalars().first().task_type == self.task_type


class CTaskFilter(Filter):
    def __init__(self, task_type: str):
        self.task_type = task_type

    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> bool:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == callback.message.chat.id))
            return result.scalars().first().task_type == self.task_type


class GotPrize(Filter):

    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> bool:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == callback.message.chat.id))
            return bool(result.scalars().first().prize_id)


class MIsAdmin(Filter):

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return message.chat.id in [268241744, 490082094]


class CIsAdmin(Filter):

    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> bool:
        return callback.message.chat.id in [268241744, 490082094]
