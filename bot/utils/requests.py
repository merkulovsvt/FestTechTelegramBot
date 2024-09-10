from sqlalchemy import select

from bot.utils.models import async_session, User


async def add_user_if_not_exists(chat_id: int, username: str):
    async with async_session() as session:
        print(chat_id)
        result = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        existing_user = result.scalars().first()

        if existing_user:
            print(f"User {username} already exists in the database.")
        else:
            new_user = User(chat_id=chat_id, username=username)
            session.add(new_user)
            await session.commit()
            print(f"User {username} added successfully.")


async def change_task_type(chat_id: int, task_type: str):
    async with async_session() as session:
        print(chat_id)
        result = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        existing_user = result.scalars().first()
        existing_user.task_type = task_type
        await session.commit()


async def participate_in_lottery(chat_id: int):
    async with async_session() as session:
        print(chat_id)
        result = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        existing_user = result.scalars().first()
        if existing_user.participates_in_lottery:
            print("User is already participating in lottery.")  # TODO
        else:
            existing_user.participates_in_lottery = True
            await session.commit()
