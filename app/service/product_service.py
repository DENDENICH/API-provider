from typing import Optional, Type
from .base_service import BaseService, Model

class ProductService(BaseService):
    def __init__(
        self,
        name: str,
        category: str,
        article_number: str,
        organizer_id: int,
        price: float,
        id_: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.name = name
        self.category = category
        self.article_number = article_number
        self.organizer_id = organizer_id
        self.price = price
