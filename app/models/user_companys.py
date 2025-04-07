from typing import TypedDict
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class UserCompanyDict(TypedDict):
    id: int
    user_id: int
    role: str
    organizer_id: int


class UserCompany(Base):
    """Сущность привязанной учетной записи пользователя в компании"""

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    role: Mapped[str] = mapped_column(
        String(255),
        Enum("admin", "manager", "employee",
            name="user_role_enum"
        ),
        nullable=False
    )
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=True
    )

    organizer = relationship(
        "Organizer", 
        back_populates="employee",
        foreign_keys=[organizer_id]
    )
    user = relationship(
        "User", 
        back_populates="user_company",
        foreign_keys=[user_id]
    )

    @property
    def dict(self):
        return UserCompanyDict(
            id=self.id,
            user_id=self.user_id,
            role=self.role,
            organizer_id=self.organizer_id,
        )
    

        