from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .annotades import intpk

class SuppliesProduct(Base):
    """Объект поставки"""
    __tablename__ = 'supplies_product'

    id: Mapped[intpk]
    supply_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('supplies.id'),
        index=True,
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('product.id'),
        index=True,
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )