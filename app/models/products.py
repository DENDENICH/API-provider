from typing import TypedDict
from sqlalchemy import (
    String,
    CheckConstraint,
    Text,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ProductsDict(TypedDict):
    id: int
    name: str
    category: str
    description: str
    price: float
    supplier_id: int
    supplier: object  # TODO: исправить анотацию
    supply_products: object  # TODO: исправить анотацию


class Product(Base):
    """Таблица товаров"""

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
            'tools_and_equipment'
            )""",
            name="product_category"
        )
    )
    description: Mapped[str] = mapped_column(
        Text
    )
    price: Mapped[str]  = mapped_column(
        Numeric,
        nullable=False
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )

    #relationship
    supplier = relationship("Organizer", back_populates="products")
    supply_products = relationship("SupplyProduct", back_populates="product")

    def dict(self):
        return ProductsDict(
            id=self.id,
            name=self.name,
            category=self.category,
            description=self.description,
            price=self.price,
            supplier_id=self.supplier_id
        )
    