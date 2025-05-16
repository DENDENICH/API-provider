from dataclasses import dataclass
from typing import Optional, Type, Iterable

from .base import Model, BaseItem


class ProductVersionItem(BaseItem):
    """Бизнес-объект сущности версии продукта"""
    def __init__(
        self,
        name: str,
        category: str,
        price: float,
        description: str = None,
        img_path: str = None,
        id: Optional[int] = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.img_path = img_path


@dataclass
class ProductCreate:
    name: str
    category: str
    price: float
    quantity: int
    description: str = None,
    img_path: str = None # Пока не участвует


class ProductItem(BaseItem):
    """Бизнес-объект сущности продукта"""
    def __init__(
        self,
        article: int = None,
        product_version_id: int = None,
        supplier_id: int = None,
        id: int = None,
        model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)

        self.article = article
        self.product_version_id = product_version_id
        self.supplier_id = supplier_id


class AvailableProductForCompany(BaseItem):
    """Представление объекта продукта, разрешенного для компании"""
    def __init__(
            self,
            id: int,
            article: int,
            name: str,
            category: str,
            price: float,
            organizer_name: str,
            supplier_id: int,
            quantity: Optional[int] = None,
            img_path: Optional[str] = None
    ):
        self.article = article
        self.name = name
        self.category = category
        self.price = price
        self.organizer_name = organizer_name
        self.supplier_id = supplier_id
        self.quantity = quantity
        self.img_path = img_path


class ProductFullItem(BaseItem):
    """Представление полной версии продукта с свойствами версии продукта"""
    def __init__(
            self,
            article: int,
            name: str,
            category: str,
            price: float,
            description: str = None,
            img_path: str = None,
            id: int = None, 
            model: Optional[Type[Model]] = None
        
        ):
        super().__init__(id, model)

        self.article = article
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.img_path = img_path


def get_ids_from_products_version(
        products: Iterable[ProductVersionItem]
) -> Iterable[int]:
    """Получить список id продуктов из списка версий продуктов"""
    return [product.id for product in products]