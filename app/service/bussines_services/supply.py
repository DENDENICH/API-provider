from typing import List, Optional, Iterable
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import (
    SupplyProductRepository,
    SupplyRepository,
)
from service.items_services.supply import (
    SupplyResponseItem,
    SupplyCreateItem,
    SupplyItem, 
    SupplyProductItem,
    SupplyStatus,
    get_supply_item_by_supply_create_item,
    get_supply_product_items
)
from service.items_services.product import get_ids_from_products_version, ProductItem
from service.items_services.expense import ExpenseAddReservedItem, ExpenseSupplierItem

from service.redis_service import UserDataRedis

from service.bussines_services.contract import ContractService
from service.bussines_services.product import ProductService
from service.bussines_services.expense.expense_supplier import ExpenseSupplierService


from exceptions import NotFoundError, BadRequestError

from utils import generate_unique_code


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"

class CancelledAssembleStatus(str, Enum):
    cancelled = "cancelled"
    assemble = "assemble"


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
            raise BadRequestError("not found contract")
        return 


    async def create_supply(
            self, 
            supply: SupplyCreateItem,
    ) -> None:
        """Создать поставку"""
        supply_item = await self._create_supply_and_flush_session(
            supply=get_supply_item_by_supply_create_item(supply)
        )
        products_ids = supply.get_products_ids
        products_version_ids = await self._get_products_version_ids_by_products_ids(
            products_ids=products_ids
        )
        supply_products_item = get_supply_product_items(
            supply_id=supply_item.id,
            quantities=supply.get_quantities,
            products_version_ids=products_version_ids
        )
        await self._create_supplies_products_and_flush_session(
            supply=supply_products_item
        )
        await self._update_reversed_in_expense_and_flush_session(
            supplier_id=supply_item.supplier_id,
            supply=supply_products_item,
            products_ids=products_ids
        )
        return
    
    async def _get_products_version_ids_by_products_ids(
            self,
            products_ids: Iterable[int]
    ) -> Iterable[int]:
        """Получить список версий продуктов"""
        product_service = ProductService(self.session)
        product_versions = await product_service.get_products_version_by_product_ids(
            product_ids=products_ids
        )
        return get_ids_from_products_version(product_versions)
    
    async def _update_reversed_in_expense_and_flush_session(
            self, 
            supplier_id: int,
            supply: Iterable[SupplyProductItem],
            products_ids: Iterable[int]
    ) -> Iterable[ExpenseSupplierItem]:
        """Обновить расход с зарезервированным количеством"""
        expense_service = ExpenseSupplierService(self.session)
        # Инкапсулировать данную логику в ExpenseService или объекте ExpenseSupplierItem
        expense_list = []
        # TODO: извлечь продукты спомощью сервиса продуктов по объектам SupplyProductItem
        for supply_product, product_id in zip(supply, products_ids):
            expense = ExpenseAddReservedItem(
                supplier_id=supplier_id,
                product_id=product_id,
                reserved=supply_product.quantity
            )
            expense_update = await expense_service.add_reserved_expense(
                add_reverved_expense=expense
            )
            expense_list.append(expense_update)

        await self.session.flush()
        return expense_list
        
    async def _create_supply_and_flush_session(
            self,
            supply: SupplyItem
    ) -> SupplyItem:
        """Создать поставку и зафиксировать изменения в сессии"""
        article = generate_unique_code()
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
    

    async def get_all_supplies_by_user_data(
            self, 
            user_data: UserDataRedis,
            is_wait_confirm: bool = False
    ) -> List[SupplyResponseItem]:
        """Получить все доступные поставки пользователя по его данным"""
        if user_data.organizer_role == OrganizerRole.supplier:
            supplies = await self._get_supplies_by_organizer_id(
                supplier_id=user_data.organizer_id,
                is_wait_confirm=is_wait_confirm
            )
        elif user_data.organizer_role == OrganizerRole.company:
            supplies = await self._get_supplies_by_organizer_id(
                company_id=user_data.organizer_id
            )
        else:
            raise BadRequestError("not found organizer role")
        return supplies
    
    async def _get_supplies_by_organizer_id(
            self,
            company_id: Optional[int] = None,
            supplier_id: Optional[int] = None,
            is_wait_confirm: bool = False
    ) -> List[SupplyResponseItem]:
        """Получить все поставки"""
        supplies = await self.supply_repo.get_all_by_organizer_id(
            company_id=company_id,
            supplier_id=supplier_id,
            is_wait_confirm=is_wait_confirm
        )
        if not supplies:
            raise NotFoundError("not found supplies")
        return supplies


    async def assemble_or_cancel_supply(self, supplier_id: int, status: SupplyStatus) -> None:
        """Принять или отменить поставку"""

        supply: SupplyItem = await self.supply_repo.get_by_id(status.id)
        if not supply:
            raise NotFoundError("not found supply")
        
        supply.is_wait_confirm = False
        supply.status = status.status
        await self._update_supply_by_supplier_id_and_flush_session(
            supplier_id=supplier_id,
            supply=supply
        )
        # возврат расходов
        await self._update_quantity_and_reversed_expenses_by_status(
            supplier_id=supplier_id,
            supply=supply,
            status=status,
        )
        return
    
    async def _get_products_by_supplies(self, supplies):
        # извлечение продуктов их поставок
        pass

    async def update_supply_status(self, supplier_id: int, status: SupplyStatus) -> SupplyItem:
        """Обновить статус поставки"""
        supply: SupplyItem = await self.supply_repo.get_by_id(status.id)
        if not supply:
            raise NotFoundError("not found supply")
        
        supply.status = status.status
        
        return await self._update_supply_by_supplier_id_and_flush_session(
            supplier_id=supplier_id,
            supply=supply
        )
    
    async def _update_supply_by_supplier_id_and_flush_session(
            self, 
            supplier_id: int, 
            supply: SupplyItem
    ) -> SupplyItem:
        supply_update = await self.supply_repo.update(
            obj=supply, 
            supplier_id=supplier_id
        )
        if not supply_update:
            raise NotFoundError("not found supply")
        await self.session.flush()
        return supply_update

    async def _update_quantity_and_reversed_expenses_by_status(
            self,
            supplier_id: int,
            supply: SupplyItem,
            status: SupplyStatus
    ) -> Iterable[ExpenseSupplierItem]:
        """Обновить расходы по сущности поставки взависимости от статуса"""
        # TODO: реализация работы со складом. 
        # Если поставка принимается: 
        #   - списать у резерва кол-во каждого товара в поставке
        #   - списать у кол-ва товара на складе кол-во товара в поставке
        # Если поставка отклоняется: 
        #   - списать у резерва кол-во каждого товара в поставке
        supply_products: Iterable[SupplyProductItem] = await self.supply_product_repo.get_by_supply_id(
            supply_id=supply.id
        )
        product_service = ProductService(self.session)
        products: Iterable[ProductItem] = await product_service.get_products_by_supplies_products(
            supplies_products=supply_products
        )
        products_ids = [p.id for p in products]

        expenses_list = list()
        expense_service = ExpenseSupplierService(self.session)

        for supply_product, product_id in zip(supply_products, products_ids):
            expense = await expense_service.get_expense_by_id_supplier_and_product(
                supplier_id=supplier_id,
                product_id=product_id
            )

            expense.reserved -= supply_product.quantity
            if status.status == CancelledAssembleStatus.assemble:
                expense.quantity -= supply_product.quantity

            expense_update = await expense_service.update_expense(expense)
            expenses_list.append(expense_update)

        return expenses_list
