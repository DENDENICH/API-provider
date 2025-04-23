from typing import TypedDict
from sqlalchemy import (
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ProductDict(TypedDict):
    id: int
    article: str
    product_version_id: int
    supplier_id: int


class Product(Base):
    """Таблица товаров"""

    article: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True
    )
    product_version_id: Mapped[int] = mapped_column(
        ForeignKey("product_versions.id", ondelete="CASCADE"),
        nullable=False
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )
    
    #relationship
    supplier = relationship(
        "Organizer", 
        back_populates="product",
        foreign_keys=[supplier_id]
    )
    product_version = relationship(
        "ProductVersion", 
        back_populates="product",
        foreign_keys=[product_version_id]    
    )
    expense_supplier = relationship(
        "ExpenseSupplier",
        back_populates="product",
        foreign_keys="[ExpenseSupplier.product_id]"
    )

    @property
    def dict(self):
        return ProductDict(
            id=self.id,
            article=self.article,
            product_version_id=self.product_version_id,
            supplier_id=self.supplier_id
        )
    