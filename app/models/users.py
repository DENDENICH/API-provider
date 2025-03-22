from typing import TypedDict
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class UserDict(TypedDict):
    id: int
    role: str
    name: str
    email: str
    phone: str
    password: bytes
    organizer_id: int


class User(Base):
    """Таблица пользователей"""

    role: Mapped[str] = mapped_column(
        String(255),
        Enum("admin", "manager", "employee",
            name="user_role_enum"
        ),
        nullable=False
    )
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
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )

    organizer = relationship("Organizer", back_populates="employees")

    

    @property
    def dict(self):
        return UserDict(
            id=self.id,
            name=self.name,
            role=self.role,
            email=self.email,
            phone=self.phone,
            password=self.password,
            organizer_id=self.organizer_id,
        )
    

        