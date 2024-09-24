import asyncio
import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from sqlalchemy import select

from bot.handlers import user_handlers, info_handlers, contest_handlers
from bot.middlewares.user_activity import UserActivity
from bot.utils.config import start_bot, stop_bot
from bot.utils.models import async_main
from bot.utils.models import async_session, User

load_dotenv()


async def main():
    await async_main()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)

    dp = Dispatcher(storage=RedisStorage.from_url(url=os.getenv("REDIS_URL")))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(user_handlers.router, info_handlers.router, contest_handlers.router)
    dp.update.outer_middleware(UserActivity())

    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(notify, 'interval', minutes=1, args=[bot])
    # scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def notify(bot: Bot):
    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                (User.last_activity < datetime.now() - timedelta(minutes=20)) &
                (User.notification_check == False) &
                (User.task_type != "complete")))

        inactive_users = result.scalars().all()
        for user in inactive_users:
            try:
                await bot.send_message(chat_id=user.chat_id,
                                       text="Вы не активны более 20 минут! Квест сам себя не пройдёт! 🎉")

                user.notification_check = True
            except Exception as e:
                print(f"{user.username} has blocked the bot")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
