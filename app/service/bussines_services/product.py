from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import *
from service.items_services.items import *
from service.redis_service import redis

from exceptions import not_found_error

from utils import generate_unique_code



class ProductService:
    """Класс бизнес-логики работы с товарами"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session=session)
        self.version_repo = ProductVersionRepository(session=session)

    async def create_product(
            self,
            id: int, 
            name: str,
            category: str,
            price: float,
            description: str,
    ) -> ProductItem:
        """_summary_

        Args:
            id (int): Идентификатор пользователя
            name (str): Название продукта
            category (str): Категория продукта
            price (float): Цена продукта
            description (str): Описание продукта
            img_file (str): Ссылка на файл

        Returns:
            ProductItem: _description_
        """

        article = await generate_unique_code()

        # TODO: сделать реализацию сохранения картинки 
        img_file = None

        # Создаем версию продукта
        product_version_item = ProductItem(
            name=name,
            category=category,
            description=description,
            price=price,
            img_path=img_file
        )
        product_version: ProductItem = await self.version_repo.create(product_version_item)
        await self.session.flush()

        # Создаем продукт
        temp_product = ProductItem(
            article=article,
            product_version_id=product_version.id,
            supplier_id=id,
        )
        product: ProductItem = await self.product_repo.create(temp_product)
        await self.session.flush()

        return product
    
    async def get_all_products(self, supplier_id: int) -> list[ProductItem]:
        """Получить все продукты поставщика"""
        if (products := await self.product_repo.get_all_products(supplier_id=supplier_id)) is None:
            raise not_found_error
        return products
    
    async def get_product_by_id(self, product_id: int) -> Optional[ProductItem]:
        """Получить продукт по id"""
        if (product := await self.product_repo.get_by_id(id=product_id)) is None:
            raise not_found_error
        return product
    
    async def update_product(
            self, 
            product_id: int,
            product: ProductItem
        ) -> ProductItem: 
        """Обновить продукт"""
        if (user_item := await self.product_repo.update(
            obj_id=product_id,
            obj=product
            )
        ) is None:
            raise not_found_error
        return user_item
    