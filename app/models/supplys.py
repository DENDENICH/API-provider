from typing import TypedDict
from sqlalchemy import (
    String,
    Enum,
    Integer,
    ForeignKey,
    Text,
    Numeric,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class SuppliesDict(TypedDict):
    id: int
    article: int
    supplier_id: int
    company_id: int
    status: str
    delivery_address: str
    total_price: float


class Supply(Base):
    """Поставки"""

    # Уникальный артикул поставки
    article: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )
    supplier_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String,
        Enum(
            'in_processing', 
            'assembled',
            'in_delivery',
            'delivered',
            'adopted',
            'canceled',
            name="status_supplies"
        ),
        nullable=False,
    )
    is_assembled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )
    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )
    delivery_address: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    total_price: Mapped[float] = mapped_column(
        Numeric,
        nullable=False
    )

    #relationship
    supplier = relationship("Organizer", back_populates="supplies_as_supplier", foreign_keys=[supplier_id])
    company = relationship("Organizer", back_populates="supplies_as_company", foreign_keys=[company_id])
    supply_products = relationship("SupplyProduct", back_populates="supply")

    @property
    def dict(self):
        return SuppliesDict(
            id=self.id,
            article=self.article,
            supplier_id=self.supplier_id,
            company_id=self.company_id,
            status=self.status,
            delivery_address=self.delivery_address,
            total_price=self.total_price
        )
    