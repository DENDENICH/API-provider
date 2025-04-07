from typing import TypedDict
from sqlalchemy import (
    String,
    Float,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ProductVersionDict(TypedDict):
    id: int
    product_id: int
    name: str
    category: str
    price: float
    img_path: str 


class ProductVersion(Base):
    """Версия товара"""

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), 
        nullable=False
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
    price: Mapped[float] = mapped_column(
        Float, 
        nullable=False
    )
    img_path: Mapped[str] = mapped_column(
        String, 
        nullable=True
    )

    product = relationship(
        "Product", 
        back_populates="product_version",
        foreign_keys="[Product.product_version_id]"    
    )
    supply_products = relationship(
        "SupplyProduct", 
        back_populates="product_version",
        foreign_keys="[SupplyProduct.product_version_id]"
    )
    expense_company = relationship(
        "ExpenseCompany",
        back_populates="product_version",
        foreign_keys="[ExpenseCompany.product_version_id]"
    )

    @property
    def dict(self):
        return ProductVersionDict(
            id=self.id,
            product_id=self.product_id,
            name=self.name,
            category=self.category,
            price=self.price,
            img_path=self.img_path
        )
    