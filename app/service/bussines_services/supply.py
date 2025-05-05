from typing import List, Optional, Iterable
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import (
    SupplyProductRepository,
    SupplyRepository
)
from app.service.items_services.supply import (
    SupplyResponseItem,
    SupplyCreateItem,
    SupplyItem, 
    SupplyProductItem,
    ProductInSupplyCreate,
    SupplyStatus,
    get_supply_item_by_supply_create_item,
    get_supply_product_items
)
from service.items_services.product import get_ids_from_products_version

from service.redis_service import UserDataRedis

from service.bussines_services.contract import ContractService
from service.bussines_services.product import ProductService


from exceptions import not_found_error, bad_request_error

from utils import generate_unique_code


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


class SupplyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.supply_repo = SupplyRepository(session=session)
        self.supply_product_repo = SupplyProductRepository(session=session)

    async def check_is_contract_exist(
            self, 
            company_id: int,
            supplier_id: int
    ) -> None:
        """Проверка существования контракта между компанией и поставщиком"""
        contract_service = ContractService(self.session)
        if await contract_service.get_contract_by_company_and_supplier_id(
                company_id=company_id,
                supplier_id=supplier_id
        ) is None:
            raise bad_request_error("not found contract")
        return 


    async def _get_products_version_ids_by_products_ids(
            self,
            products_ids: Iterable[int]
    ) -> Iterable[int]:
        """Получить список версий продуктов"""
        product_service = ProductService(self.session)
        product_versions = await product_service.get_products_version_by_product_ids(
            products_ids=products_ids
        )
        return get_ids_from_products_version(product_versions)
        
    async def _create_supply_and_flush_session(
            self,
            supply: SupplyItem
    ) -> SupplyItem:
        """Создать поставку и зафиксировать изменения в сессии"""
        article = await generate_unique_code(self.session, self.supply_repo.model, "article")
        supply.article = article
        supply = await self.supply_repo.create(supply)
        await self.session.flush()
        return supply

    async def _create_supplies_products_and_flush_session(
            self,
            supply: Iterable[SupplyProductItem]
    ) -> None:
        """Создать продукты в поставке и зафиксировать изменения в сессии"""
        await self.supply_product_repo.create_all(supply)
        await self.session.flush()
        return

    async def create_supply(
            self, 
            supply: SupplyCreateItem
    ) -> None:
        """Создать поставку"""

        supply_item = await self._create_supply_and_flush_session(
            supply=get_supply_item_by_supply_create_item(supply)
        )

        supply_products_item = get_supply_product_items(
            supply_id=supply_item.id,
            quantities=supply.get_quantities,
            products_version_ids=await self._get_products_version_ids_by_products_ids(
                products_ids=supply.get_products_ids
            )
        )

        await self._create_supplies_products_and_flush_session(
            supply=supply_products_item
        )
        return
    
    
    async def _get_supplies_by_organizer_id(
            self,
            company_id: Optional[int] = None,
            supplier_id: Optional[int] = None        
    ) -> List[SupplyResponseItem]:
        """Получить все поставки"""
        supplies = await self.supply_repo.get_all_by_organizer_id(
            company_id=company_id,
            supplier_id=supplier_id
        )
        if not supplies:
            raise not_found_error("not found supplies")
        return supplies

    async def get_all_supplies_by_user_data(self, user_data: UserDataRedis) -> List[SupplyResponseItem]:
        """Получить все доступные поставки пользователя по его данным"""
        if user_data.organizer_role == OrganizerRole.supplier:
            supplies = await self._get_supplies_by_organizer_id(
                supplier_id=user_data.organizer_id
            )
        elif user_data.organizer_role == OrganizerRole.company:
            supplies = await self._get_supplies_by_organizer_id(
                company_id=user_data.organizer_id
            )
        return supplies


    async def assemble_or_cancel_supply(self, supplier_id: int, status: SupplyStatus) -> None:
        """Принять или отменить поставку"""
        supply: SupplyItem = await self.supply_repo.get_by_id(status.id)
        if not supply:
            raise not_found_error("not found supply")
        supply.is_wait_confirm = False
        supply.status = status.status
        if (supply_update := await self.supply_repo.update(
                obj=supply, 
                supplier_id=supplier_id
            )
        ) is None:
            raise not_found_error("not found supply")
        return


    async def update_supply_status(self, supplier_id: int, status: SupplyStatus) -> None:
        """Обновить статус поставки"""
        supply: SupplyItem = await self.supply_repo.get_by_id(status.id)
        if not supply:
            return None
        supply.status = status.status
        # TODO: возвращать обновленную поставку, сделав запрос на получение supply по id
        if (supply_update := await self.supply_repo.update(
                obj=supply, 
                supplier_id=supplier_id
            )
        ) is None:
            raise not_found_error("not found supply")
        return
