from typing import TypedDict
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class LinkCodeDict(TypedDict):
    id: int
    user_id: int
    code: int


class LinkCode(Base):
    """Таблица для хранения ключей-привязок уч. записей пользователей к компаниям"""

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    code: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user = relationship(
        "User", 
        back_populates="link_code",
        foreign_keys=[user_id]    
    )

    @property
    def dict(self):
        return LinkCodeDict(
            id=self.id,
            user_id=self.user_id,
            code=self.code
        )
    

        