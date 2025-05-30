from typing import Optional, Iterable, List
from sqlalchemy.ext.asyncio import AsyncSession

from service.items_services.items import SupplyProductItem

from service.repositories import (
    ProductRepository,
    ProductVersionRepository,
)
from service.items_services.product import (
    ProductVersionItem,
    ProductCreate,
    ProductItem,
    ProductFullItem,
    AvailableProductForCompany
)
from service.items_services.expense import ExpenseSupplierItem, ExpenseWithInfoProductItem
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
            product_new: ProductCreate
    ) -> ExpenseWithInfoProductItem:
        """Создание продукта"""
        product_version = await self._create_version_product_and_flush_session(
            data=ProductVersionItem(
                name=product_new.name,
                category=product_new.category,
                price=product_new.price,
                description=product_new.description
            )
        )
        product = await self._create_product_and_flush_session(
            ProductItem(
                article=generate_unique_code(),
                product_version_id=product_version.id,
                supplier_id=user_data.organizer_id,
            )
        )
        new_expense = await self._create_expense_by_product_and_flush_session(
            supplier_id=user_data.organizer_id,
            product_id=product.id,
            quantity=product_new.quantity
        )
        return ExpenseWithInfoProductItem(
            article=product.article,
            product_id=product.id,
            product_name=product_version.name,
            category=product_version.category,
            quantity=new_expense.quantity,
            description=product_version.description,
            id=new_expense.id
        )
    
    async def _create_version_product_and_flush_session(
            self, 
            data: ProductVersionItem
    ) -> ProductVersionItem:
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
    
    async def _create_expense_by_product_and_flush_session(
            self,
            supplier_id: int,
            product_id: int,
            quantity: int
    ) -> ExpenseSupplierItem:
        expense_service = ExpenseSupplierService(session=self.session)
        new_expense = await expense_service.add_expense(
            expense=ExpenseSupplierItem(
                supplier_id=supplier_id,
                product_id=product_id,
                quantity=quantity
            )
        )
        await self.session.flush()
        return new_expense
    
    
    async def get_available_products_for_company(
            self, 
            company_id: int,
            supplier_id: Optional[int] = None,
            add_quantity: bool = False
    ) -> List[AvailableProductForCompany]:
        """Получить все продукты поставщиков для компании"""
        products: List[AvailableProductForCompany] = await self.product_repo.get_available_products_for_company(
                company_id=company_id,
                supplier_id=supplier_id,
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
    ) -> Iterable[ProductVersionItem]:
        """Получить все версии продуктов по id"""
        if (products_version := await self.version_repo.get_products_version_by_products_ids(product_ids)) is None:
            raise not_found_error
        return products_version
    
    async def get_products_by_supplies_products(
            self,
            supplies_products: Iterable[SupplyProductItem]
    ) -> Iterable[ProductItem]:
        """Получить все продукты по продуктам в поставках"""
        if (products := await self.product_repo.get_products_by_supplies_products(supplies_products)) is None:
            raise not_found_error
        return products
    

    async def update_product(
            self, 
            product_id: int,
            product_version: ProductVersionItem
        ) -> ExpenseWithInfoProductItem: 
        """Обновить данные продукта"""
        product: ProductItem = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise not_found_error
        
        new_product_version = await self._create_version_product_and_flush_session(
            product_version
        )
        product.product_version_id = new_product_version.id
        product = await self.product_repo.update(product)

        expense_service = ExpenseSupplierService(self.session)
        expense = await expense_service.get_expense_by_id_supplier_and_product(
            supplier_id=product.supplier_id,
            product_id=product.id
        )

        return ExpenseWithInfoProductItem(
            id=expense.id,
            article=product.article,
            product_id=product.id,
            product_name=product_version.name,
            category=product_version.category,
            quantity=expense.quantity,
            description=product_version.description,
        )
    
    async def delete_product(
            self, 
            product_id: int
        ) -> None:
        """Удалить продукт"""
        product: ProductItem = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise not_found_error
        
        await self.product_repo.delete(product.id)
        await self.session.flush()
        