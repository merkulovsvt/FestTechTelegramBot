import os
from datetime import datetime
from pathlib import Path

from aiogram import Bot

BASE_DIR = Path(__file__).resolve().parent.parent.parent


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=os.getenv("MODERATOR_CHAT_ID"),
                           text=f"Бот запущен {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=os.getenv("MODERATOR_CHAT_ID"),
                           text=f"Бот остановлен {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")
