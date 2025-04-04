from typing import TypedDict
from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ExpenseDict(TypedDict):
    id: int
    company_id: int
    product_version_id: int
    quantity: int


class ExpenseCompanys(Base):
    """Товары на складе компании"""

    company_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id"),
        nullable=False
    )
    product_version_id: Mapped[int] = mapped_column(
        ForeignKey("product_versions.id"), 
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    product_version = relationship("ProductVersion")

    @property
    def dict(self):
        return ExpenseDict(
            id=self.id,
            company_id=self.company_id,
            product_version_id=self.product_version_id,
            quantity=self.quantity,
        )

