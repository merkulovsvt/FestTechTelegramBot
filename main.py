import asyncio
import logging
import os

from bot.utils.models import async_main
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from bot.handlers import user_handlers, info_handlers, contest_handlers

load_dotenv()

storage = RedisStorage.from_url(url=os.getenv("CELERY_URL"))


async def main():
    await async_main()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher(storage=storage)
    dp.include_routers(user_handlers.router, info_handlers.router, contest_handlers.router)

    # await bot.set_my_commands([BotCommand(command="/start", description="Start")])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
