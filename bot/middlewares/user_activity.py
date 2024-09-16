from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.utils.requests import update_user_activity


class UserActivity(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await update_user_activity(
            chat_id=event.message.chat.id if event.message else event.callback_query.message.chat.id,
            username=event.message.chat.username if event.message else event.callback_query.message.chat.username)

        result = await handler(event, data)

        # if not get_flag(data, 'handled') and event.message:
        #     await event.message.answer("Я тебя не понимаю 😔")

        return result
