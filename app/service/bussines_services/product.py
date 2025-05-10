from typing import Optional, Iterable, List
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
from service.bussines_services.expense.expense_supplier import ExpenseSupplierService
from service.redis_service import UserDataRedis

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
    
    
    async def get_available_products_for_company(
            self, 
            company_id: int,
            supplier_id: Optional[int] = None,
            add_quantity: Optional[bool] = False
    ) -> List[AvailableProductForCompany]:
        """Получить все продукты поставщиков для компании"""
        products: List[AvailableProductForCompany] = await self.product_repo.get_available_products_for_company(
                company_id=company_id,
                supplier_id=supplier_id,
                add_quantity=add_quantity
            )
        if products is None:
            raise not_found_error
        if add_quantity:
            products = await self._get_quantity_for_products(products)
        return products
    
    async def _get_quantity_for_products(
            self,
            products: List[AvailableProductForCompany],
    ) -> List[AvailableProductForCompany]:
        """Получить количество для продуктов"""
        expense_service = ExpenseSupplierService(self.session)
        for product in products:
            expense = await expense_service.get_expense_by_id_supplier_and_product(
                supplier_id=product.supplier_id,
                product_id=product.id
            )
            product.quantity = expense.get_quantity_subtract_reserve  
        return products  


    async def get_product_by_id(self, product_id: int) -> Optional[ProductFullItem]:
        """Получить продукт по id"""
        if (product := await self.product_repo.get_by_id_full_product(product_id)) is None:
            raise not_found_error
        return product
    

    async def get_products_version_by_product_ids(
            self, 
            product_ids: Iterable[int]
    ) -> Iterable[ProductVersion]:
        """Получить все версии продуктов по id"""
        if (products_version := await self.version_repo.get_products_version_by_products_ids(product_ids)) is None:
            raise not_found_error
        return products_version
    

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
        