from typing import TypedDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class UserDict(TypedDict):
    id: int
    name: str
    email: str
    phone: str
    password: bytes


class User(Base):
    """Таблица пользователей"""

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
    )
    phone: Mapped[str] = mapped_column(
        String(255),
    )
    password: Mapped[bytes] = mapped_column(
        String,
        nullable=False
    )


    user_company = relationship("UserCompany", back_populates="user")
    link_code = relationship("LinkCode", back_populates="user")

    
    @property
    def dict(self):
        return UserDict(
            id=self.id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            password=self.password,
        )
    
