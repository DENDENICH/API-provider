from typing import Optional, Type

from .base import Model, BaseItem


class OrganizerItem(BaseItem):
    """Объект организации"""
    def __init__(self,
                 role: str,
                 name: str,
                 address: str,
                 inn: str,
                 bank_details: str,
                 id: Optional[int] = None, 
                 model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.role = role
        self.address = address
        self.name = name
        self.inn = inn
        self.bank_details = bank_details


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


class UserItem(BaseItem):
    """Объект сущности пользователя"""
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        password: str,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password


class UserCompanyItem(BaseItem):
    """Объект сущности уч. записи пользователя компании"""
    def __init__(
        self,
        organizer_id: int,
        user_id: int,
        role: str,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.organizer_id = organizer_id
        self.user_id = user_id
        self.role = role


class LinkCodeItem(BaseItem):
    """Объект сущности пригласительного кода"""
    def __init__(
        self,
        code: int,
        user_id: int,
        id: Optional[int] = None, 
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.user_id = user_id
        self.code = code


class ProductItem(BaseItem):
    """Объект продукта с полями версии продукта"""
    def __init__(
        self,
        article: int,
        product_version_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        name: Optional[str] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        img_path: Optional[str] = None,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.article = article
        self.product_version_id = product_version_id
        self.supplier_id = supplier_id
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.img_path = img_path


class SupplyItem(BaseItem):
    """Объект сущности поставки"""
    def __init__(
        self,
        article: int,
        supplier_id: int,
        company_id: int,
        status: str,  # "в обработке", "собран", "в доставке", "доставлен"
        delivery_address: str,
        total_price: float = 0.0,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.article = article
        self.supplier_id = supplier_id
        self.company_id = company_id
        self.status = status
        self.delivery_address = delivery_address
        self.total_price = total_price
        # свойство - список supply products

class SupplyProductItem(BaseItem):
    """Объект записи продукта в поставке"""
    def __init__(
        self,
        supply_id: int,
        product_version_id: int,
        quantity: int,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.supply_id = supply_id
        self.product_id = product_version_id
        self.quantity = quantity


class ExpenseCompanyItem(BaseItem):
    """Объект сущности отчета и склада компании"""
    def __init__(
        self,
        company_id: int,
        product_version_id: int,
        quantity: int,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.product_version_id = product_version_id
        self.company_id = company_id
        self.quantity = quantity


class ExpenseSupplierItem(BaseItem):
    """Объект сущности отчета и склада поставщика"""
    def __init__(
        self,
        supplier_id: int,
        product_id: int,
        quantity: int,
        reserved: int,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.supplier_id = supplier_id
        self.product_id = product_id
        self.quantity = quantity
        self.reserved = reserved


__all__ = [
    "OrganizerItem",
    "ContractItem",
    "UserItem",
    "UserCompanyItem",
    "LinkCodeItem",
    "ProductItem",
    "SupplyItem",
    "SupplyProductItem",
    "ExpenseCompanyItem",
    "ExpenseSupplierItem"
]
