from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import ContactRepository
from service.items_services.organizer import OrganizerItem
from service.items_services.contract import ContractItem

from service.bussines_services.contract import ContractService

from exceptions.exceptions import BadRequestError, NotFoundError


class SupplierService:
    """Класс бизнес-логики для работы с организацией"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.contract_repo = ContactRepository(self.session)
    
    async def create_contract(
        self,
        contract_item: ContractItem
    ) -> ContractItem:
        """Создать контракт"""
        await self._check_exists_contract(
            company_id=contract_item.company_id, 
            supplier_id=contract_item.supplier_id
        )
        return await self.contract_repo.create(contract_item)
    
    async def _check_exists_contract(self, company_id: int, supplier_id: int) -> None:
        """Проверка на существование контракта между компанией и поставщиком"""
        contract_service = ContractService(session=self.session)
        if await contract_service.get_contract_by_company_and_supplier_id(
            company_id=company_id, 
            supplier_id=supplier_id
        ):
            raise BadRequestError("Contract already exists")


    async def get_supplier_available_company(self, company_id: int) -> List[OrganizerItem]:
        """Получение поставщиков"""
        suppliers: List[OrganizerItem] = await self.contract_repo.get_supplier_available_company(company_id=company_id)
        if not suppliers:
            raise NotFoundError("Suppliers not found")
        return suppliers

    async def delete_contract(
        self,
        supplier_id: int,
        company_id: int,
    ) -> None:
        """Удалить контракт"""
        try:
            result = await self.contract_repo.delete(
                supplier_id=supplier_id,
                company_id=company_id
            )
            if not result:
                raise BadRequestError("Suppliers not found")
        except Exception as e:
            pass
        