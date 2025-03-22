from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


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

    def dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "company_id": self.company_id
        }
    