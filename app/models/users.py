from sqlalchemy import String,  CheckConstraint, BINARY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .annotades import intpk


class Users(Base):
    """Таблица пользователей"""
    __tablename__ = ['users']

    id: Mapped[intpk]
    role: Mapped[str] = mapped_column(
        String(255),
        CheckConstraint(
            "role IN ('admin', 'employee')"
        )
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    password: Mapped[bytes] = mapped_column(
        BINARY,
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id")
    )