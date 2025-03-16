from sqlalchemy import (
    String,
    CheckConstraint,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .annotades import intpk


class Supplies(Base):
    """Поставки"""
    __tablename__ = 'supplies'

    id: Mapped[intpk]
    supplier_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizers.id'),
        index=True,
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizers.id'),
        index=True,
        nullable=False
    )
    status: Mapped[intpk] = mapped_column(
        String,
        CheckConstraint(
            """status IN (
            'in_processing', 
            'assembled',
            'in_delivery',
            'delivered',
            'adopted'
            )"""
        ),
        nullable=False,
    )