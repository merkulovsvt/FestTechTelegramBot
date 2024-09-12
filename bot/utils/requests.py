import random
from datetime import datetime

from sqlalchemy import select

from bot.utils.models import async_session, User, StudyUser, ExpertUser, LotteryPrizes


# User requests
async def update_user_activity(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.last_activity = datetime.now()
        existing_user.notification_check = False
        await session.commit()


async def add_user_if_not_exists(chat_id: int, username: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        existing_user = result.scalars().first()
        if not existing_user:
            new_user = User(chat_id=chat_id, username=username)
            session.add(new_user)
            await session.commit()


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


async def get_prize(chat_id: int):
    async with async_session() as session:
        available_prizes = session.execute(
            select(LotteryPrizes).where(LotteryPrizes.quantity > 0)
        ).scalars().all()

        if not available_prizes:
            return {}

        prize = random.choice(available_prizes)

        user = await session.execute(
            select(User).where(User.chat_id == chat_id)).scalars().first()

        user.prize_id = prize.id
        prize.quantity -= 1

        await session.commit()
        return prize.to_dict()


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

async def set_study_name(chat_id: int, username: str, name: str):
    async with async_session() as session:
        result = await session.execute(
            select(StudyUser).where(StudyUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        if existing_user:
            existing_user.name = name
        else:
            session.add(StudyUser(chat_id=chat_id, username=username, name=name))

        await session.commit()


async def set_study_program(chat_id: int, program: str):
    async with async_session() as session:
        result = await session.execute(
            select(StudyUser).where(StudyUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.program = program
        await session.commit()


async def set_study_contact(chat_id: int, contact: str):
    async with async_session() as session:
        result = await session.execute(
            select(StudyUser).where(StudyUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.contact = contact
        await session.commit()


# ExpertUser requests

async def set_expert_name(chat_id: int, username: str, name: str):
    async with async_session() as session:
        result = await session.execute(
            select(ExpertUser).where(ExpertUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        if existing_user:
            existing_user.name = name
        else:
            session.add(ExpertUser(chat_id=chat_id, username=username, name=name))
        await session.commit()


async def set_expert_area_of_expertise(chat_id: int, area_of_expertise: str):
    async with async_session() as session:
        result = await session.execute(
            select(ExpertUser).where(ExpertUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.area_of_expertise = area_of_expertise
        await session.commit()


async def set_expert_place_of_work(chat_id: int, place_of_work: str):
    async with async_session() as session:
        result = await session.execute(
            select(ExpertUser).where(ExpertUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.place_of_work = place_of_work
        await session.commit()


async def set_expert_contact(chat_id: int, contact: str):
    async with async_session() as session:
        result = await session.execute(
            select(StudyUser).where(StudyUser.chat_id == chat_id))
        existing_user = result.scalars().first()
        existing_user.contact = contact
        await session.commit()
