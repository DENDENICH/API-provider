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
ClassItemObj = TypeVar("ClassItemObj")


class BaseRepository(Generic[Model]):
    def __init__(
            self, 
            model: Type[Model], 
            item: Type[ClassItemObj],
            session: AsyncSession,
            # to_item: Optional[
            #     Callable[
            #         [dict, ItemObj, Optional[Model]], 
            #         ItemObj
            #     ]
            # ] = None
    ):
        self.model = model
        self.session = session
        self.item = item
        # self.to_item = to_item


    async def get_all(self) -> List[Type[ItemObj]]:
        """ Получить все записи """
        result = await self.session.execute(select(self.model))
        items = [self.item(**model.dict, model=model) for model in result.scalars()]
        return items


    async def get_by_id(self, id: int) -> Optional[Type[ItemObj]]:
        """ Получить объект по ID """
        result = await self.session.execute(
            select(self.model)
            .filter(self.model.id == id)
        )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


    async def create(self, obj: Type[ItemObj]) -> Type[ItemObj]:
        """Создать объект """
        model = self.model(**obj.dict)
        self.session.add(model)
        return self.item(**model.dict, model=model)


    async def update(
            self, 
            obj: Type[ItemObj],
            obj_id: Optional[int] = None, 
    ) -> Optional[Type[ItemObj]]:
        """ Обновить объект по ID """
        query = update(self.model).where(
            self.model.id == obj_id or self.model.id == obj.id
        ).values(**obj.dict).returning(self.model)
        
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


    async def delete(self, obj_id: int) -> Optional[Type[ItemObj]]:
        """ Удалить объект по ID """
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


# def payload_to_item(
#         payload: dict, 
#         obj_item: Type[ItemObj], 
#         model: Optional[Type[Model]] = None
# ) -> ItemObj:
#     """
#     Универсальная функция для создания бизнес-объекта из словаря
#     """
#     return obj_item(**payload, model_=model)