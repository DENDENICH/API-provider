from typing import TypedDict
from sqlalchemy import (
    String,
    Integer,
    Enum,
    Text,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ProductDict(TypedDict):
    id: int
    article: str
    name: str
    category: str
    description: str
    price: str
    supplier_id: int


class Product(Base):
    """Таблица товаров"""

    article: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(255),
        Enum(
            'hair_coloring', 
            'hair_care',
            'hair_styling',
            'consumables',
            'perming',
            'eyebrows_and_eyelashes',
            'manicure_and_pedicure',
            'tools_and_equipment',
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
    img_path: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    #relationship
    supplier = relationship("Organizer", back_populates="products")
    supply_products = relationship("SupplyProduct", back_populates="product")

    def dict(self):
        return ProductDict(
            id=self.id,
            article=self.article,
            name=self.name,
            category=self.category,
            description=self.description,
            price=self.price,
            supplier_id=self.supplier_id
        )
    