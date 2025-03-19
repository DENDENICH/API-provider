from typing import Optional, Type
from .base_service import BaseService, Model

class SupplyProductService(BaseService):
    def __init__(
        self,
        supply_id: int,
        product_id: int,
        quantity: int,
        id_: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.supply_id = supply_id
        self.product_id = product_id
        self.quantity = quantity