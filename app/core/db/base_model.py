from datetime import datetime

from sqlalchemy import MetaData, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .core import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    """Класс для наследования в ORM модели"""
    pass

    #добавление уникальных значений для всех уникальных и др. значений при инициализации моделей и миграции
    metadata = MetaData( 
        naming_convention=settings.database.naming_conventions
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @property
    def dict(self):
        """Представление модели ввиде словаря"""

