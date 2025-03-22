from typing import TypedDict

from sqlalchemy import String,  Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA


from core.db import Base


class OrganizersDict(TypedDict):
    id: int
    role: str
    name: str
    address: str
    inn: int
    bank_details: bytes


class Organizer(Base):
    """Таблица организаций"""

    role: Mapped[str] = mapped_column(
        String(255),
        Enum("company", "supplier", name="organizer_role"),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    inn: Mapped[str]  = mapped_column(
        String(255),
        nullable=False
    )
    bank_details: Mapped[bytes] = mapped_column(
        String,
        nullable=False
    )

    #relationship
    # Связь Product.supplier & Organizer.products если Organizer.role == "supplier"
    products = relationship("Product", back_populates="supplier", foreign_keys="[Product.supplier_id]")

    expenses = relationship("Expenses", back_populates="organizer")
    
    # Связь поля Organizer.employees с User.organizers для взаимного обновления
    employees = relationship("User", back_populates="organizer")
    supplies_as_company = relationship("Supply", back_populates="company", foreign_keys="[Supply.company_id]")
    supplies_as_supplier = relationship("Supply", back_populates="supplier", foreign_keys="[Supply.supplier_id]")

    contract_as_company = relationship("Contract", back_populates="company")
    contract_as_supplier = relationship("Contract", back_populates="supplier")

    def dict(self):
        return OrganizersDict(
            id=self.id,
            role=self.role,
            name=self.name,
            address=self.address,
            inn=self.inn,
            bank_details=self.bank_details,
        )
    