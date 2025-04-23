from typing import Optional, Type

from .base import Model, BaseItem


# class ProductItem(BaseItem):
#     """Объект продукта с полями версии продукта"""
#     def __init__(
#         self,
#         article: Optional[int] = None,
#         product_version_id: Optional[int] = None,
#         supplier_id: Optional[int] = None,
#         name: Optional[str] = None,
#         category: Optional[str] = None,
#         description: Optional[str] = None,
#         price: Optional[float] = None,
#         img_path: Optional[str] = None,
#         id: Optional[int] = None,
#         model: Optional[Type[Model]] = None
#     ):
#         super().__init__(id=id, model=model)

#         self.article = article
#         self.product_version_id = product_version_id
#         self.supplier_id = supplier_id
#         self.name = name
#         self.category = category
#         self.description = description
#         self.price = price
#         self.img_path = img_path


class ProductVersion(BaseItem):
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


class AvailableProductForCompany:
    """Представление объекта продукта, разрешенного для компании"""
    def __init__(
            self,
            id: int,
            article: int,
            name: str,
            category: str,
            price: float,
            organizer_name: str,
            img_path: str = None
    ):
        self.id = id
        self.article = article
        self.name = name
        self.category = category
        self.price = price
        self.organizer_name = organizer_name
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
