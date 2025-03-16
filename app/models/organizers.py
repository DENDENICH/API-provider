from sqlalchemy import String,  CheckConstraint, BINARY
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .annotades import intpk


class Organizers(Base):
    __table__ = ['organizers']

    id: Mapped[intpk]
    role: Mapped[str] = mapped_column(
        String(255),
        CheckConstraint(
            ("company", "supplier")
        )
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    inn: Mapped[str]  = mapped_column(
        String(255),
        nullable=False
    )
    bank_details: Mapped[bytes] = mapped_column(
        BINARY,
        nullable=False
    )