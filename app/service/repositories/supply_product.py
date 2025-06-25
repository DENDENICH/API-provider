from typing import Optional, List, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import SupplyProduct as SupplyProductModel
from service.repositories.base_repository import BaseRepository

from service.items_services.supply import SupplyProductItem



class SupplyProductRepository(BaseRepository[SupplyProductModel]):
    """Репозиторий бизнес логики работы c продуктом в поставке"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(SupplyProductModel, session=session, item=SupplyProductItem)

    async def create_all(
            self,
            products: Iterable[SupplyProductItem]
    ) -> None:
        """Создать объекты"""
        models = [self.model(**product.dict) for product in products]
        self.session.add_all(models)

    async def get_by_supply_id(
            self,
            supply_id: int
    ) -> Optional[List[SupplyProductItem]]:
        """Получить продукты из поставок по id поставки"""
        stmt = (
            select(self.model)
            .where(self.model.supply_id == supply_id)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.item(**model.dict) for model in models] if models is not None else None
