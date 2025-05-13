from typing import Optional, Type, Iterable
from dataclasses import dataclass

from service.items_services.base import Model, BaseItem

from service.items_services.product import ProductVersion

from schemas.supply import SupplyCreateRequest


@dataclass
class SupplyStatus:
    id: int
    status: str


@dataclass
class OrganizerInfoInSupply:
    id: int
    name: str

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    article: int

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "article": self.article
        }


@dataclass
class ProductInSupply:
    product: Product
    quantity: int

    @property
    def dict(self):
        return {
            "product": self.product.dict(),
            "quantity": self.quantity
        }


@dataclass
class ProductInSupplyCreate:
    product_id: int
    quantity: int


class SupplyItem(BaseItem):
    """Объект сущности поставки"""
    def __init__(
        self,
        supplier_id: int,
        company_id: int,
        delivery_address: str,
        total_price: float,
        is_wait_confirm: bool = True,
        status: str = 'in_processing',
        article: Optional[int] = None,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.supplier_id = supplier_id
        self.status = status
        self.delivery_address = delivery_address
        self.total_price = total_price
        self.is_wait_confirm = is_wait_confirm
        self.article = article


class SupplyCreateItem(SupplyItem):
    """Объект сущности создания поставки"""
    def __init__(
        self,
        supplier_id: int,
        company_id: int,
        delivery_address: str,
        total_price: float,
        article: Optional[int] = None,
        supply_products: Optional[Iterable[ProductInSupplyCreate]] = None,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(
            supplier_id=supplier_id,
            company_id=company_id, 
            delivery_address=delivery_address, 
            total_price=total_price, 
            article=article,
            id=id, 
            model=model
        )
        
        self.supply_products = supply_products

    @classmethod
    def get_supply_create_item_by_schema_and_company_id(
            cls,
            schema: SupplyCreateRequest,
            company_id: int
    ) -> "SupplyCreateItem":
        return cls(
            supplier_id=schema.supplier_id,
            company_id=company_id,
            delivery_address=schema.delivery_address,
            total_price=schema.total_price,
            supply_products=tuple(
                ProductInSupplyCreate(
                    product_id=product.product_id,
                    quantity=product.quantity
                ) for product in schema.supply_products
            )
        )
    
    @property
    def get_products_ids(self) -> Iterable[int]:
        """Получить список id продуктов в поставке"""
        return [product.product_id for product in self.supply_products]
    
    @property
    def get_quantities(self) -> Iterable[int]:
        """Получить список количеств продуктов в поставке"""
        return [product.quantity for product in self.supply_products]


class SupplyResponseItem(BaseItem):
    """Объект сущности поставки"""
    def __init__(
        self,
        article: Optional[int],
        supplier: OrganizerInfoInSupply,
        company: OrganizerInfoInSupply,
        status: str, 
        is_wait_confirm: bool,
        delivery_address: str,
        total_price: float,
        supply_products: Optional[Iterable[ProductInSupply]],
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.article = article
        self.supplier = supplier
        self.company = company
        self.supply_products = supply_products
        self.status = status
        self.delivery_address = delivery_address
        self.total_price = total_price
        self.is_wait_confirm = is_wait_confirm

    @classmethod
    def get_from_dict(cls, data: dict) -> "SupplyResponseItem":
        """Получить объект из словаря"""
        return cls(
            article=data.get("article"),
            supplier=OrganizerInfoInSupply(
                id=data["supplier"]["id"],
                name=data["supplier"]["name"]
            ),
            company=OrganizerInfoInSupply(
                id=data["company"]["id"],
                name=data["company"]["name"]
            ),
            status=data["status"],
            is_wait_confirm=data["is_wait_confirm"],
            delivery_address=data["delivery_address"],
            total_price=data["total_price"],
            supply_products=[
                ProductInSupply(
                    product=Product(**product["product"]),
                    quantity=product["quantity"]
                ) for product in data["supply_products"]
            ]
        )
    
    # алгоритм данного метода нужно реализовать и в методе dict базового класса BaseItem
    @property
    def dict(self):
        dict_supply_response = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, OrganizerInfoInSupply):
                dict_supply_response[key] = value.dict
            if isinstance(value, list):
                dicts_products = [product.dict for product in value]
                dict_supply_response[key] = dicts_products
            else:
                dict_supply_response[key] = value

        return dict_supply_response
      


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
        self.product_version_id = product_version_id
        self.quantity = quantity


#TODO: исправить данный костыль: 
# найти способ перенести данный функции в классы поставок

def get_supply_item_by_supply_create_item(supply: SupplyCreateItem) -> SupplyItem:
    """Получить объект поставки из объекта создания поставки"""
    return SupplyItem(
        supplier_id=supply.supplier_id,
        delivery_address=supply.delivery_address,
        total_price=supply.total_price,
        article=supply.article,
        id=supply.id
    )


def get_supply_product_items(
        supply_id: int,
        products_version_ids: Iterable[int],
        quantities: Iterable[int],
):
    """Получить список объектов записи продукта в поставке"""
    return [
        SupplyProductItem(
            supply_id=supply_id,
            product_version_id=product_version_id,
            quantity=quantity
        )
        for product_version_id, quantity in zip(products_version_ids, quantities)
    ]