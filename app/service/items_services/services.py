from typing import Optional, Type

from .base_service import BaseService, Model


class UserService(BaseService):
    """Бизнес объект пользователя"""
    def __init__(self,
                 role: str,
                 name: str,
                 email: str,
                 phone: str,
                 password: str,
                 company_id: int,
                 id: Optional[int] = None, 
                 model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)
        
        self.role = role
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.company_id = company_id


class SupplyService(BaseService):
    """Бизнес объект поставки"""
    def __init__(
        self,
        article: int,
        supplier_id: int,
        company_id: int,
        status: str,  # "в обработке", "собран", "в доставке", "доставлен"
        delivery_address: str,
        total_price: float = 0.0,
        id: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)
        
        self.article = article
        self.supplier_id = supplier_id
        self.company_id = company_id
        self.status = status
        self.delivery_address = delivery_address
        self.total_price = total_price


class SupplyProductService(BaseService):
    """Бизнес объект записи продукта в поставке"""
    def __init__(
        self,
        supply_id: int,
        product_id: int,
        quantity: int,
        id: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)
        
        self.supply_id = supply_id
        self.product_id = product_id
        self.quantity = quantity


class OrganizerService(BaseService):
    """Бизнес объект организации"""
    def __init__(self,
                 role: str,
                 name: str,
                 address: str,
                 inn: str,
                 bank_details: str,
                 id: Optional[int] = None, 
                 model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)
        
        self.role = role
        self.address = address
        self.name = name
        self.inn = inn
        self.bank_details = bank_details


class ExpenseService(BaseService):
    """Бизнес объект отчета продукции"""
    def __init__(
        self,
        organizer_id: int,
        product_id: int,
        quantity: int,
        id: Optional[int] = None,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)
        
        self.organizer_id = organizer_id
        self.product_id = product_id
        self.quantity = quantity


class ProductsDict(BaseService):
    """Бизнес объект продукта"""
    def __init__(
        self,
        article: int,
        name: str,
        category: str,
        description: str,
        price: float,
        supplier_id: int,
        id: int,
        model_: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model_=model_)

        self.article = article
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.supplier_id = supplier_id