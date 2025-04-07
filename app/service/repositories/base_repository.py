from typing import (
    Type,
    TypeVar,
    Generic, 
    List,
    Optional,
    Callable
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from core.db import Base 
from service.items_services.base import BaseItem


Model = TypeVar("Model", bound=Base)  # Тип данных для моделей
ItemObj = TypeVar("ItemObj", bound=BaseItem) # Тип данных для объектов бизнес логики


class BaseRepository(Generic[Model]):
    def __init__(
            self, 
            model: Type[Model], 
            session: AsyncSession,
            to_item: Callable[[Model], ItemObj]
    ):
        self.model = model
        self.session = session
        self.to_item = to_item


    async def get_all(self) -> List[ItemObj]:
        """ Получить все записи """
        result = await self.session.execute(select(self.model))
        items = [self.to_item(model) for model in result.scalars()]
        return items


    async def get_by_id(self, obj_id: int) -> Optional[ItemObj]:
        """ Получить объект по ID """
        result = await self.session.execute(select(self.model).filter(self.model.id == obj_id))
        model = result.scalar_one_or_none()
        return self.to_item(model) if model is not None else None


    async def create(self, obj: ItemObj) -> ItemObj:
        """Создать объект """
        model = self.model(**obj.dict)
        self.session.add(model)
        return self.to_item(model)


    async def update(self, obj: ItemObj) -> Optional[ItemObj]:
        """ Обновить объект по ID """
        query = update(self.model).where(self.model.id == obj.id).values(**obj.dict).returning(self.model)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self.to_item(model) if model is not None else None


    async def delete(self, obj_id: int) -> None:
        """ Удалить объект по ID """
        query = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
