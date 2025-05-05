from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import ContactRepository
from service.items_services.items import ContractItem


class ContractService:
    """Класс бизнес-логики работы с сущностями контракта"""
    def __init__(self, session: AsyncSession):
        self.contract_repo = ContactRepository(
            session=session, 
        )

    async def get_contract_by_company_and_supplier_id(
            self, 
            company_id: int,
            supplier_id: int
        ) -> Optional[ContractItem]:
        """Получение контракта по id компании и поставщика"""
        return await self.contract_repo.get_by_company_and_supplier_id(
            company_id=company_id,
            supplier_id=supplier_id
        )

        