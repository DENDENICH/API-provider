from typing import TypedDict
from sqlalchemy import String, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ExpenseDict(TypedDict):
    id: int
    organizer_id: int
    product_id: int
    quantity: int

    organizer: object # TODO: исправить анотацию
    product: object # TODO: исправить анотацию



class Expense(Base):
    __tablename__ = "expenses"

    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"), 
        nullable=False
        )  

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), 
        nullable=False
        )  

    quantity: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    organizer = relationship("Organizer", back_populates="expenses")
    product = relationship("Product")

    def dict(self):
        return ExpenseDict(
            id=self.id,
            organizer_id=self.organizer_id,
            product_id=self.product_id,
            quantity=self.quantity
        )


