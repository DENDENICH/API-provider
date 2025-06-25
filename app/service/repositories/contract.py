from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Organizer as OrganizerModel,
    Contract as ContractModel,
)
from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.organizer import OrganizerItem
from service.items_services.contract import ContractItem


class ContactRepository(BaseRepository[ContractModel]):
    """Репозиторий бизнес логики работы с контрактами"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ContractModel, session=session, item=ContractItem)

    async def get_by_company_and_supplier_id(self, company_id: int, supplier_id: int) -> Optional[ContractItem]:
        """Получение контракта по id компании и поставщика"""
        stmt = select(self.model).filter(
                self.model.company_id == company_id,
                self.model.supplier_id == supplier_id
            )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_supplier_available_company(self, company_id: int) -> List[OrganizerItem]:
        """Получить поставщиков с которыми заключены контракты"""
        stmt = (
            select(OrganizerModel)
            .join(self.model, self.model.supplier_id == OrganizerModel.id)
            .where(self.model.company_id == company_id)
        )
        result = await self.session.execute(stmt)
        suppliers = result.scalars().all()
        # рассмотреть перенос данного метода в логику организации
        return [OrganizerItem(**supplier.dict, model=supplier) for supplier in suppliers]

    async def delete(self, supplier_id: int, company_id: int) -> bool:
        """Удалить контракт по id поставщика"""
        stmt = (
            delete(self.model)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.company_id == company_id
            )
        )
        result = await self.session.execute(stmt)
        # Возвращаем False, если результат изменения = 0
        return False if result.rowcount == 0 else True