from app.database.models import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Schedule
from sqlalchemy import select, update, delete

from aiogram import Bot, Dispatcher, types


async def set_user(tg_id: int, async_session: AsyncSession):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()


async def add_schedule_entry(session: AsyncSession, user_id: int, day_name: str, subject: str):
    async with session.begin():  # Начинаем транзакцию
        new_entry = Schedule(
            user_id=user_id, day_name=day_name, subject=subject)
        session.add(new_entry)
        await session.commit()


async def get_user_schedule_by_day(session, user_id: int, day_name: str):
    # Выполняем асинхронный запрос для получения расписания
    result = await session.execute(
        select(Schedule.subject)
        .filter_by(user_id=user_id, day_name=day_name)
    )
    # Извлекаем результаты как список строк
    schedule = result.scalars().all()
    return schedule


async def delete_user_schedule(session: AsyncSession, user_id: int):
    async with session.begin():
        await session.execute(delete(Schedule).where(Schedule.user_id == user_id))
