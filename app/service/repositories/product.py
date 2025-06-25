from typing import Optional, List, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Organizer as OrganizerModel,
    Contract as ContractModel,
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
)
from service.repositories.base_repository import(
     BaseRepository,
)

from service.items_services.product import (
    ProductItem,
    ProductFullItem,
    AvailableProductForCompany
)


from service.items_services.supply import SupplyProductItem


class ProductRepository(BaseRepository[ProductModel]):
    """Репозиторий бизнес логики работы с товаром"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ProductModel, session=session, item=ProductItem)

    async def get_by_id_full_product(self, id: int) -> AvailableProductForCompany:
        """Получить объект по ID"""
        stmt = (
            select(
                self.model.id,
                self.model.article,
                self.model.supplier_id,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.img_path,
                ProductVersionModel.description,
                OrganizerModel.name.label("organizer_name")
            )
            .join(ProductVersionModel, ProductVersionModel.id == self.model.product_version_id )
            .join(OrganizerModel, OrganizerModel.id == self.model.supplier_id)
            .where(self.model.id == id)
        )
        result = await self.session.execute(stmt)
        product = result.mappings().first()
        return AvailableProductForCompany(**dict(product)) if product is not None else None

    async def get_by_product_version_id(self, product_version_id: int) -> ProductItem:
        """Получить продукт по id версии"""
        stmt = (
            select(self.model)
            .where(
                self.model.product_version_id == product_version_id
            )
        )
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return ProductItem(**product.dict)

    async def get_all_products(
            self,
            supplier_id: int,
            limit: int = 20
    ) -> Optional[List[ProductFullItem]]:
        """Получение всех продуктов"""
        stmt = (
            select(
                self.model.id,
                self.model.article,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.img_path
            )
            .join(ProductVersionModel, self.model.product_version_id == ProductVersionModel.id)
            .where(self.model.supplier_id == supplier_id)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        products = result.mappings().all()

        if products is None:
            return None

        products = [ProductFullItem(**dict(p)) for p in products]

        return products

    async def get_available_products_for_company(
            self,
            company_id: int,
            supplier_id: Optional[int] = None,
            limit: int = 100
    ) -> Optional[List[AvailableProductForCompany]]:
        """Получить все доступные товары для компании по её ID"""
        stmt = (
            select(
                self.model.id,
                self.model.article,
                self.model.supplier_id,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.img_path,
                OrganizerModel.name.label("organizer_name")
            )
            .join(ProductVersionModel, ProductVersionModel.id == self.model.product_version_id )
            .join(OrganizerModel, OrganizerModel.id == self.model.supplier_id)
            .join(ContractModel, ContractModel.supplier_id == self.model.supplier_id)
            .where(ContractModel.company_id == company_id ,)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        products = result.mappings().all()

        if products is None:
            return None
        if supplier_id:
            products = [
                AvailableProductForCompany(**dict(p))
                for p in products if p.get("supplier_id") == supplier_id
            ]
        else:
            products = [
                AvailableProductForCompany(**dict(p))
                for p in products
            ]
        return products

    async def get_products_by_supplies_products(
            self,
            supply_products: Iterable[SupplyProductItem]
    ) -> Iterable[ProductItem]:
        """Получить все продукты по id продуктов в поставке"""
        products_version_ids = [supply_product.product_version_id for supply_product in supply_products]
        stmt = (
            select(self.model)
            .where(self.model.product_version_id.in_(products_version_ids))
        )
        result = await self.session.execute(stmt)
        products: Iterable[ProductModel] = result.scalars().all()
        return [self.item(**p.dict) for p in products]