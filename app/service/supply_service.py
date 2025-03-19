from typing import Optional, Type
from .base_service import BaseService, Model

class SupplyService(BaseService):
    def __init__(
        self,
        supplier_id: int,
        company_id: int,
        status: str,  # "в обработке", "собран", "в доставке", "доставлен"
        delivery_address: str,
        total_price: float = 0.0,
        id_: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.supplier_id = supplier_id
        self.company_id = company_id
        self.status = status
        self.delivery_address = delivery_address
        self.total_price = total_price
