import random
from datetime import datetime

from sqlalchemy import select, distinct
from sqlalchemy.orm import selectinload

from bot.utils.models import async_session, User, StudyUser, ExpertUser, LotteryPrize


# User requests
async def update_user_activity(chat_id: int, username: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))

        user = result.scalars().first()

        if user:
            user.last_activity = datetime.now()
            user.notification_check = False
        else:
            new_user = User(chat_id=chat_id, username=username)
            session.add(new_user)
        await session.commit()


async def get_all_chat_ids():
    async with async_session() as session:
        result = await session.execute(
            select(distinct(User.chat_id)))
        return [row[0] for row in result.fetchall()]


async def change_task_type(chat_id: int, task_type: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.task_type = task_type
        await session.commit()


async def get_task_type(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        existing_user = result.scalars().first()
        return existing_user.task_type


async def set_prize(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(LotteryPrize).options(selectinload(LotteryPrize.company)).where(LotteryPrize.quantity > 0)
        )

        available_prizes = result.scalars().all()

        if not available_prizes:
            return {}

        prize = random.choice(available_prizes)

        result = await session.execute(
            select(User).where(User.chat_id == chat_id))

        user = result.scalars().first()

        user.prize_id = prize.id
        prize.quantity -= 1

        data = {
            "id": prize.id,
            "name": prize.name,
            "company_id": prize.company.id,
            "company_name": prize.company.name,
            "company_url": prize.company.url,
        }

        await session.commit()

        return data


async def get_prize(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))

        user = result.scalars().first()

        result = await session.execute(
            select(LotteryPrize).options(selectinload(LotteryPrize.company)).where(LotteryPrize.id == user.prize_id)
        )

        prize = result.scalars().first()

        data = {
            "id": prize.id,
            "name": prize.name,
            "company_id": prize.company.id,
            "company_name": prize.company.name,
            "company_url": prize.company.url,
        }

        await session.commit()

        return data


async def set_lottery_participation(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        result.scalars().first().participate_in_lottery = True
        await session.commit()


async def participate_in_lottery(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        return result.scalars().first().participate_in_lottery


async def got_prize(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        return bool(result.scalars().first().prize_id)


# StudyUser requests

async def set_student_data(chat_id: int, **kwargs):
    async with async_session() as session:
        result = await session.execute(
            select(StudyUser).where(StudyUser.chat_id == chat_id))
        study_user = result.scalars().first()

        if study_user:
            for key, value in kwargs.items():
                if hasattr(study_user, key):
                    setattr(study_user, key, value)
        else:
            session.add(StudyUser(chat_id=chat_id, **kwargs))

        await session.commit()


# ExpertUser requests

async def set_expert_data(chat_id: int, **kwargs):
    async with async_session() as session:
        result = await session.execute(
            select(ExpertUser).where(ExpertUser.chat_id == chat_id))
        expert_user = result.scalars().first()

        if expert_user:
            for key, value in kwargs.items():
                if hasattr(expert_user, key):
                    setattr(expert_user, key, value)
        else:
            session.add(ExpertUser(chat_id=chat_id, **kwargs))

        await session.commit()


# Рандомайзер

async def get_random_user():
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.participate_in_lottery == 1))
        users = result.scalars().all()
        winner_username = random.choice(users).username
        await session.commit()
        return winner_username
