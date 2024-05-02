from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="start-handler-router")


@router.message(CommandStart())
async def get_start_cmd(message: Message, state: FSMContext, session: AsyncSession, user):
    await message.answer("Команда старт получена")
    await message.answer(str(user))
