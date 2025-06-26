from typing import Optional, Type, Iterable
from dataclasses import dataclass

from service.items_services.base import Model, BaseItem

from exceptions import BadRequestError


class ExpenseWithInfoProductItem(BaseItem):
    """Объект расхода с полями версии продукта"""
    def __init__(
        self,
        article: int,
        product_id: int,
        product_name: str,
        category: str,
        quantity: int,
        supplier_name: Optional[str] = None,
        description: Optional[str] = None,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.article = article
        self.product_id = product_id
        self.supplier_name = supplier_name
        self.product_name = product_name
        self.quantity = quantity
        self.category = category
        self.description = description

    @property
    def dict(self):
        base_dict = super().dict
        base_dict.update({"id": self._id})
        return base_dict


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


    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if isinstance(value, (int, float)):
            if value < 0:
                raise BadRequestError("Negative quantity")
            self._quantity = value
        else:
            raise BadRequestError("Error type a quantity")
        
    @property
    def reserved(self):
        return self._reserved
    
    @reserved.setter
    def reserved(self, value):
        if isinstance(value, (int, float)):
            if value < 0:
                raise BadRequestError("Negative reserved")
            elif value > self.quantity:
                raise BadRequestError("Oversupply of reserved")
            self._reserved = value
        else:
            raise BadRequestError("Error type a reserved")


    @property
    def get_quantity_subtract_reserve(self) -> int:
        """Количество расхода с вычитом резерва"""
        return self.quantity - self.reserved
    
    @property
    def dict(self):
        base_dict = super().dict
        base_dict.update(
            {
                "quantity": self.quantity,
                "reserved": self.reserved
            }
        )
        return base_dict
    

@dataclass
class ExpenseAddReservedItem(BaseItem):
    """Объект добавления резерва расхода"""
    supplier_id: int
    product_id: int
    reserved: int


@dataclass
class ExpenseUpdateQuantityItem:
    """Объект обновления количества"""
    organizer_id: int
    expense_id: int
    quantity: int
