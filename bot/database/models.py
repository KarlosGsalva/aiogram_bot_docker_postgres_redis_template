from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func

from bot.database.db import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(32), nullable=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=True)
    language_code = Column(String(8), nullable=True, comment="Telegram client's lang")

    is_admin = Column(Boolean, default=False)
    is_moderator = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'@{self.username}' if self.username else f'{self.user_id}'

