from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship

from bot.utils.config import BASE_DIR

engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR}/FestTechBot.db")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    username = Column(String, unique=True)

    task_type = Column(String, unique=False, default='')
    prize_id = Column(Integer, default=None)
    participate_in_lottery = Column(Boolean, default=False)

    last_activity = Column(DateTime, default=datetime.now())
    notification_check = Column(Boolean, default=False)


class StudyUser(Base):
    __tablename__ = 'study_users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    username = Column(String, unique=True)

    name = Column(String)
    program = Column(String)
    contact = Column(String)


class ExpertUser(Base):
    __tablename__ = 'expert_users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    username = Column(String, unique=True)

    name = Column(String)
    area_of_expertise = Column(String)
    place_of_work = Column(String)
    contact = Column(String)


class LotteryPrize(Base):
    __tablename__ = 'lottery_prizes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    quantity = Column(Integer, primary_key=False)
    company_id = Column(String, ForeignKey('companies.id'))

    company = relationship("Company")


class Company(Base):
    __tablename__ = 'companies'

    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
