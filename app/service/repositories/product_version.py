from typing import Optional, List, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
)
from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.product import ProductVersionItem


class ProductVersionRepository(BaseRepository[ProductVersionModel]):
    """Репозиторий бизнес логики работы с версией товара"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ProductVersionModel, session=session, item=ProductVersionItem)

    async def get_products_version_by_products_ids(
            self,
            products_ids: Iterable[int]
    ) -> List[ProductVersionItem]:
        """Получить все версии продуктов по id продуктов"""
        stmt = (
            select(self.model)
            .where(
                ProductModel.id.in_(products_ids),
                self.model.id == ProductModel.product_version_id
            )
        )
        result = await self.session.execute(stmt)
        products_version: Iterable[ProductVersionModel] = result.scalars().all()
        return [self.item(**p.dict) for p in products_version]

    # временно эта функция нужна для логики формирования поставки
    async def get_by_product_id(self, product_id: int) -> Optional[ProductVersionItem]:
        """Получить версию продукта по id продукта"""
        stmt = (
            select(self.model)
            .where(
                ProductModel.id == product_id,
                self.model.id == ProductModel.product_version_id
            )
        )
        result = await self.session.execute(stmt)
        products_version = result.scalar_one_or_none()
        return ProductVersionItem(**products_version.dict) if products_version else None