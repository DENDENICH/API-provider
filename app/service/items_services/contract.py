from typing import Optional, Type

from .base import Model, BaseItem


class ContractItem(BaseItem):
    """Объект сущности контракта"""
    def __init__(
        self,
        company_id: int,
        supplier_id: int,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.company_id = company_id
        self.supplier_id = supplier_id
        