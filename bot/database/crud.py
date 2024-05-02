from aiogram.types import Message, CallbackQuery

from sqlalchemy import select, update, delete, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from bot.database.models import User


async def get_or_create_user(message: Message | CallbackQuery, session: AsyncSession):
    user_id = message.from_user.id
    try:
        user = await session.execute(select(User).filter_by(user_id=user_id))
        return user.scalar_one()
    except NoResultFound:
        user = User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
        )
        session.add(user)
        await session.commit()
    return user