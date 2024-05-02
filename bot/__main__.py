import asyncio
import logging

from colorlog import ColoredFormatter

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.client.default import DefaultBotProperties

from bot.middlewares.middleware import DbSessionMiddleware
from bot.settings import config, SESSION_MAKER, DB_ENGINE
from bot.database.db import Base

from bot.handlers import start_hndlr


# ---------------

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'yellow',
        'INFO': 'green',
        'WARNING': 'cyan',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={})

for handler in logging.root.handlers:
    handler.setFormatter(color_formatter)

logger = logging.getLogger(__name__)

# ---------------

BOT_TOKEN = config.bot_token.get_secret_value()
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.update.middleware(DbSessionMiddleware(session_pool=SESSION_MAKER))
dp.callback_query.middleware(CallbackAnswerMiddleware())

dp.include_router(start_hndlr.router)


async def run_polling() -> None:
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def create_database_tables():
    Base.metadata.create_all(DB_ENGINE)


if __name__ == "__main__":
    create_database_tables()
    asyncio.run(run_polling())
