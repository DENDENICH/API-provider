from typing import Type, Generic, TypeVar, Optional
from app.core.db import Base

Model = TypeVar("Model", bound=Base)


class BaseService:
    """Базовый класс для создания бизнес объектов"""
    def __init__(self, id: Optional[int] = None, model_: Optional[Type[Model]] = None):
        self._id = id
        self._model = model_

    @property
    def get_id(self):
        return self._id or self._model.id