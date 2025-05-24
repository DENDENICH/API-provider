from typing import Type, TypeVar, Optional
from core.db import Base

Model = TypeVar("Model", bound=Base)


class BaseItem:
    """Базовый класс для создания бизнес объектов"""
    def __init__(
            self, 
            id: Optional[int] = None, 
            model: Optional[Type[Model]] = None
    ):
        self._id = id
        self._model = model

    @property
    def id(self):
        return self._id or self._model.id
    
    @property
    def dict(self):
        """Представление разрешеных свойств объекта ввиде словаря"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
