from typing import TypedDict
from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class SuppliesProductDict(TypedDict):
    id: int
    supply_id: int
    product_id: int
    quantity: int


class SupplyProduct(Base):
    """Объект поставки"""

    supply_id: Mapped[int] = mapped_column(
        ForeignKey("supplys.id", ondelete="CASCADE"),
        nullable=False
    )
    product_version_id: Mapped[int] = mapped_column(
        ForeignKey("product_versions.id", ondelete="CASCADE"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    supply = relationship(
        "Supply", 
        back_populates="supply_products",
        foreign_keys=[supply_id]
    )
    product_version = relationship(
        "ProductVersion", 
        back_populates="supply_products",
        foreign_keys=[product_version_id]   
    )

    @property
    def dict(self):
        return SuppliesProductDict(
            id=self.id,
            supply_id=self.supply_id,
            product_version_id=self.product_version_id,
            quantit=self.quantity
        )
    