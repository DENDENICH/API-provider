from typing import TypedDict
from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ContractDict(TypedDict):
    id: int
    supplier_id: int 
    company_id: int


class Contract(Base):
    """Таблица связей между компаниями и поставщиками"""

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False
    )

    company = relationship("Organizer", back_populates="contract_as_company")
    supplier = relationship("Organizer", back_populates="contract_as_supplier")

    @property
    def dict(self):
        return ContractDict(
            id=self.id,
            supplier_id=self.supplier_id,
            company_id=self.company_id
        )
    