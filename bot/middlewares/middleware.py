import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.crud import get_or_create_user

logger = logging.getLogger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            logger.debug("middleware is handling event")
            message = event.callback_query.message if event.callback_query else event.message

            if message is None:
                logger.error("Received an event without message or callback_query")
                return

            data["session"] = session
            data["user"] = await get_or_create_user(message=message, session=session)

            return await handler(event, data)
