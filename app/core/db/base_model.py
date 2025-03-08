from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from core import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    """Класс для наследования в ORM модели"""

    # добавление уникальных значений для всех уникальных и др. значений при инициализации моделей и миграции
    metadata = MetaData( 
        naming_convention=settings.database.naming_conventions
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    # вынесение общего поля
    id: Mapped[int] = mapped_column(primary_key=True)

