from typing import TypedDict
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ExpenseDict(TypedDict):
    id: int
    supplier_id: int
    product_id: int
    quantity: int
    reserved: int


class ExpenseSupplier(Base):
    """Товары на складе компании"""

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id"),
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), 
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    reserved: Mapped[int] = mapped_column(
        Integer, 
        default=0,
        nullable=False
    )

    product = relationship(
        "Product", 
        back_populates="expense_supplier",
        foreign_keys=[product_id]
    )
    supplier = relationship(
        "Organizer",
        back_populates="expense_supplier",
        foreign_keys=[supplier_id]    
    )

    @property
    def dict(self):
        return ExpenseDict(
            id=self.id,
            supplier_id=self.supplier_id,
            product_id=self.product_id,
            quantity=self.quantity,
            reserved=self.reserved
        )

