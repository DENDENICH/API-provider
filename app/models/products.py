from sqlalchemy import (
    String,
    CheckConstraint,
    Text,
    Float,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .annotades import intpk


class Products(Base):
    """Таблица товаров"""
    __tablename__ = ['products']

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(255),
        CheckConstraint(
            """role IN (
            'hair_coloring', 
            'hair_care',
            'hair_styling',
            'consumables',
            'perming',
            'eyebrows',
            'manicure_and_pedicure',
            )"""
        )
    )
    description: Mapped[str] = mapped_column(
        Text
    )
    price: Mapped[str]  = mapped_column(
        Float,
        nullable=False
    )
    supplier_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizers.id')
    )
