from typing import TypedDict
from sqlalchemy import (
    String,
    Enum,
    BigInteger,
    Integer,
    ForeignKey,
    Text,
    Numeric,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class SupplyDict(TypedDict):
    id: int
    article: int
    supplier_id: int
    company_id: int
    status: str
    is_wait_confirm: bool
    delivery_address: str
    total_price: float


class Supply(Base):
    """Поставки"""

    # Уникальный артикул поставки
    article: Mapped[int] = mapped_column(
        BigInteger,
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
    is_wait_confirm: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
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
    supplier = relationship(
        "Organizer", 
        back_populates="supplies_as_supplier", 
        foreign_keys=[supplier_id]
    )
    company = relationship(
        "Organizer", 
        back_populates="supplies_as_company", 
        foreign_keys=[company_id]
    )
    supply_products = relationship(
        "SupplyProduct", 
        back_populates="supply",
        foreign_keys="[SupplyProduct.supply_id]"
    )

    @property
    def dict(self):
        return SupplyDict(
            id=self.id,
            article=self.article,
            supplier_id=self.supplier_id,
            company_id=self.company_id,
            status=self.status,
            is_wait_confirm=self.is_wait_confirm,
            delivery_address=self.delivery_address,
            total_price=self.total_price
        )
    