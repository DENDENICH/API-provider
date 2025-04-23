from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import (
    ProductRepository,
    ProductVersionRepository
)
from service.items_services.product import (
    ProductVersion,
    ProductItem,
    ProductFullItem,
    AvailableProductForCompany
)
from service.redis_service import UserDataRedis

from exceptions import not_found_error

from utils import generate_unique_code


class ProductService:
    """Класс бизнес-логики работы с товарами"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session=session)
        self.version_repo = ProductVersionRepository(session=session)

    async def _create_version_product_and_flush_session(
            self, 
            data: ProductVersion
    ) -> ProductVersion:
        product_version = await self.version_repo.create(data)
        await self.session.flush()
        return product_version

    async def _create_product_and_flush_session(
            self, 
            data: ProductItem
    ) -> ProductItem:
        product = await self.product_repo.create(data)
        await self.session.flush()
        return product

    async def create_product(
            self,
            user_data: UserDataRedis, 
            name: str,
            category: str,
            price: float,
            description: str,
    ) -> ProductFullItem:
        #TODO: реализовать класс для группировки аргументов создания продукта
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
        product_version = await self._create_version_product_and_flush_session(
            ProductVersion(
                name=name,
                category=category,
                description=description,
                price=price,
            )
        ) 
        product = await self._create_product_and_flush_session(
            ProductItem(
                article=generate_unique_code(),
                product_version_id=product_version.id,
                supplier_id=user_data.organizer_id,
            )
        )
        return ProductFullItem(
            id=product.id,
            article=product.id,
            **product_version.dict
        )
    
    async def get_available_products_for_company(
            self, 
            company_id: int
    ) -> list[AvailableProductForCompany]:
        """Получить все продукты поставщиков для компании"""
        if (
            products := await self.product_repo.get_available_products_for_company(company_id)
        ) is None:
            raise not_found_error
        return products
    
    async def get_product_by_id(self, product_id: int) -> Optional[ProductFullItem]:
        """Получить продукт по id"""
        if (product := await self.product_repo.get_by_id_full_product(product_id)) is None:
            raise not_found_error
        return product
    
    async def update_product(
            self, 
            product_id: int,
            product_version: ProductVersion
        ) -> ProductFullItem: 
        """Обновить данные продукта"""
        product: ProductItem = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise not_found_error
        
        new_product_version = await self._create_version_product_and_flush_session(
            product_version
        )
        product.product_version_id = new_product_version.id
        product = await self.product_repo.update(product_id, product)
        return ProductFullItem(
            id=product.id,
            article=product.id,
            **new_product_version.dict
        )
        
    