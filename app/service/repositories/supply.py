from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from models import(
    Organizer as OrganizerModel,
    SupplyProduct as SupplyProductModel,
    Supply as SupplyModel,
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
)
from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.supply import (
    SupplyProductItem,
    SupplyResponseItem,
    SupplyItem,
    parse_supplies_rows
)


class SupplyRepository(BaseRepository[SupplyModel]):
    """Репозиторий бизнес логики работы с поставкой"""

    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(SupplyModel, session=session, item=SupplyItem)

    async def update(self, obj: SupplyItem, supplier_id: int) -> Optional[SupplyItem]:
        """Обновить объект поставки"""
        query = update(self.model).where(
            self.model.id == obj.id, self.model.supplier_id == supplier_id
        ).values(**obj.dict).returning(self.model)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_all_by_organizer_id(
            self,
            limit: int,
            supplier_id: Optional[int] = None,
            company_id: Optional[int] = None,
            is_wait_confirm: bool = False
    ) -> Optional[List[SupplyResponseItem]]:
        """Получить все поставки по id поставщика"""
        supplier = aliased(OrganizerModel)
        company = aliased(OrganizerModel)

        stmt = (
            select(
                self.model.id,
                self.model.article,
                self.model.delivery_address,
                self.model.total_price,
                self.model.status,
                self.model.is_wait_confirm,

                supplier.id.label("supplier_id"),
                supplier.name.label("supplier_name"),

                company.id.label("company_id"),
                company.name.label("company_name"),

                SupplyProductModel.quantity,

                ProductModel.id.label("product_id"),
                ProductModel.article.label("product_article"),
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category.label("product_category"),
                ProductVersionModel.price.label("product_price")
            )

            .join(supplier, supplier.id == self.model.supplier_id)
            .join(company, company.id == self.model.company_id)
            .join(SupplyProductModel, self.model.id == SupplyProductModel.supply_id)
            .join(ProductVersionModel, SupplyProductModel.product_version_id == ProductVersionModel.id)
            .join(ProductModel, ProductVersionModel.id == ProductModel.product_version_id)

        )

        # filters
        if company_id:
            stmt = (
                stmt.where(self.model.company_id == company_id)

                .order_by(self.model.created_at.desc())
            )
        if supplier_id:
            stmt = (
                stmt.where(
                    self.model.supplier_id == supplier_id,
                    self.model.is_wait_confirm == is_wait_confirm
                )
                .order_by(self.model.created_at.desc())
            )

        result = await self.session.execute(stmt)
        if (supplies := result.mappings().all()) is None:
            return None
        # парсим полученые объекты rows в словарь
        # TODO: исправить временную реализацию с limit
        supplies_dict_list = parse_supplies_rows(supplies, limit)
        return [SupplyResponseItem.get_from_dict(dict(supply)) for supply in supplies_dict_list]

    async def get_supply_products_by_supply_id(
            self,
            supply_id: int
    ) -> Optional[List[SupplyProductItem]]:
        """Получить все продукты в поставке по id поставки"""
        stmt = (
            select(
                SupplyProductModel.id,
                SupplyProductModel.supply_id,
                SupplyProductModel.product_version_id,
                SupplyProductModel.quantity,
                ProductModel.article.label("product_article"),
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category.label("product_category"),
                ProductVersionModel.price.label("product_price")
            )
            .join(ProductModel, ProductVersionModel.product)
            .join(ProductVersionModel, ProductVersionModel.id == ProductModel.product_version_id)
            .where(SupplyProductModel.supply_id == supply_id)
        )
        result = await self.session.execute(stmt)
        if (products := result.mappings().all()) is None:
            return None
        return [SupplyProductItem(**dict(product)) for product in products]
