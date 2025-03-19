from typing import Optional, Type
from .base_service import BaseService, Model

class ExpenseService(BaseService):
    def __init__(
        self,
        organizer_id: int,
        product_id: int,
        quantity: int,
        id_: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.organizer_id = organizer_id
        self.product_id = product_id
        self.quantity = quantity
