from typing import Optional, Type, Iterable
from dataclasses import dataclass

from .base import Model, BaseItem

from service.items_services.supply import SupplyProductItem

from exceptions import ReverseAmountError


class ExpenseWithInfoProductItem(BaseItem):
    """Объект расхода с полями версии продукта"""
    def __init__(
        self,
        article: int,
        supplier_name: str,
        product_id: int,
        product_name: str,
        category: str,
        quantity: int,
        description: Optional[str] = None,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.article = article
        self.product_id = product_id
        self.organizer_name = supplier_name
        self.product_name = product_name
        self.quantity = quantity
        self.category = category
        self.description = description
    

class ExpenseCompanyItem(BaseItem):
    """Объект сущности расхода компании"""
    def __init__(
        self,
        company_id: int,
        product_version_id: int,
        quantity: int,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.company_id = company_id
        self.product_version_id = product_version_id
        self.quantity = quantity


class ExpenseSupplierItem(BaseItem):
    """Объект сущности расхода поставщика"""
    def __init__(
        self,
        supplier_id: int,
        product_id: int,
        quantity: int,
        reserved: int = 0,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.supplier_id = supplier_id
        self.product_id = product_id
        self.quantity = quantity
        self.reserved = reserved

    def __setattr__(self, name, value):
        if name == "reserved":
            if value > self.quantity:
                raise ReverseAmountError("Oversupply of reserves")

    @property
    def get_quantity_subtract_reserve(self) -> int:
        """Количество расхода с вычитом резерва"""
        return self.quantity - self.reserved
    

@dataclass
class ExpenseAddReservedItem(BaseItem):
    """Объект добавления резерва расхода"""
    supplier_id: int
    product_id: int
    reserved: int


@dataclass
class ExpenseUpdateQuantityItem(BaseItem):
    """Объект обновления количества"""
    organizer_id: int
    expense_id: int
    quantity: int

