from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: str
    db_user: str
    db_name: str
    db_pass: str
    db_host: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()

DB_ASYNC_ENGINE = create_async_engine(url=config.db_url, echo=True)
DB_ENGINE = create_engine(config.db_url)
SESSION_MAKER = async_sessionmaker(DB_ASYNC_ENGINE, expire_on_commit=False)
