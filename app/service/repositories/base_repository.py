from typing import Type, TypeVar, Generic, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.core.db import Base 
from app.service.items_services.base_service import BaseService


Model = TypeVar("Model", bound=Base)  # Тип данных для моделей
ServiceObj = TypeVar("ServiceObj", bound=BaseService) # Тип данных для объектов бизнес логики


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session


    async def get_all(self) -> List[ServiceObj]:
        """ Получить все записи """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()


    async def get_by_id(self, obj_id: int) -> Optional[ServiceObj]:
        """ Получить объект по ID """
        result = await self.session.execute(select(self.model).filter(self.model.id == obj_id))
        return result.scalar_one_or_none()


    async def create(self, payload: dict) -> ServiceObj:
        """ Создать объект """
        obj = self.model(**payload)
        self.session.add(obj)
        # TODO: добавить возврат бизнес объекта
        return obj


    async def update(self, obj_id: int, payload: dict) -> Optional[ServiceObj]:
        """ Обновить объект по ID """
        query = update(self.model).where(self.model.id == obj_id).values(**payload).returning(self.model)
        result = await self.session.execute(query)
        # TODO: добавить возврат бизнес объекта
       
        return result.scalar_one_or_none()


    async def delete(self, obj_id: int) -> ServiceObj:
        """ Удалить объект по ID """
        query = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        # TODO: добавить возврат бизнес объекта
        result.scalar()
        return 
