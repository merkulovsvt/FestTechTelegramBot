from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///FestTechBot.db")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    participates_in_lottery = Column(Boolean, default=False)
    task_type = Column(String, unique=False, default='')


class StudyUser(Base):
    __tablename__ = 'study_users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)

    name = Column(String, unique=False, index=False)
    program = Column(String, unique=False, index=False)
    contact = Column(String, unique=False, index=False)


class ExpertUser(Base):
    __tablename__ = 'expert_users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)

    name = Column(String, unique=False, index=False)
    area_of_expertise = Column(String, unique=False, index=False)
    place_of_work = Column(String, unique=False, index=False)
    contact = Column(String, unique=False, index=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
