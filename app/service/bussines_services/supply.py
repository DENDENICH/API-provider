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
from service.items_services.product import get_ids_from_products_version
from service.items_services.expense import ExpenseAddReservedItem, ExpenseSupplierItem

from service.redis_service import UserDataRedis

from service.bussines_services.contract import ContractService
from service.bussines_services.product import ProductService
from service.bussines_services.expense.expense_supplier import ExpenseSupplierService
from service.bussines_services.expense.expense_company import (
    ExpenseCompanyItem,
    AddingExpenseCompany
)

from exceptions.exceptions import NotFoundError, BadRequestError

from utils import generate_unique_code


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"

class CancelledAssembleStatus(str, Enum):
    cancelled = "cancelled"
    assemble = "assembled"

class StatusForUpdate(str, Enum):
    assemble = "assembled"
    in_delivery = "in_delivery"
    adopted = "adopted"
    delivery = "delivery"


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
        # TODO! 
        # ПЕРЕРАБОТАТЬ ЛОГИКУ СОЗДАНИЯ ПОСТАВКИ
        # КАК МИНИМУМ НАЧАТЬ С ПРОВЕРКИ МУЩЕСТВОВАНИЯ ПРОДУКТОВ ПО ИХ ID,
        # ПОЛУЧАЕМЫХ ИЗ СХЕМЫ SUPPLY
        supply_item = await self._create_supply_and_flush_session(
            supply=get_supply_item_by_supply_create_item(supply)
        )
        products_ids = supply.get_products_ids
        # проблемное место - ids версии продуктов находятся в порядке, отличающийся от
        # продуктов
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
            limit: int = 100,
            is_wait_confirm: bool = False,
    ) -> List[SupplyResponseItem]:
        """Получить все доступные поставки пользователя по его данным"""
        if limit > 100:
            raise BadRequestError("value limit is incorrect")

        if user_data.organizer_role == OrganizerRole.supplier:
            supplies = await self._get_supplies_by_organizer_id(
                supplier_id=user_data.organizer_id,
                is_wait_confirm=is_wait_confirm,
                limit=limit
            )
        elif user_data.organizer_role == OrganizerRole.company:
            supplies = await self._get_supplies_by_organizer_id(
                company_id=user_data.organizer_id,
                limit=limit
            )
        else:
            raise BadRequestError("not found organizer role")
        return supplies
    
    async def _get_supplies_by_organizer_id(
            self,
            limit: int,
            company_id: Optional[int] = None,
            supplier_id: Optional[int] = None,
            is_wait_confirm: bool = False
    ) -> List[SupplyResponseItem]:
        """Получить все поставки"""
        supplies = await self.supply_repo.get_all_by_organizer_id(
            company_id=company_id,
            supplier_id=supplier_id,
            is_wait_confirm=is_wait_confirm,
            limit=limit
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
        # реализовать возврат расходов
        await self._update_quantity_and_reversed_expenses_by_status(
            supplier_id=supplier_id,
            supply=supply,
            status=status,
        )
        return


    async def update_supply_status(self, supplier_id: int, status: SupplyStatus) -> SupplyItem:
        """Обновить статус поставки"""
        supply: SupplyItem = await self.supply_repo.get_by_id(status.id)
        if not supply:
            raise NotFoundError("not found supply")
        
        # переместить в запрос where или отдельную бизнес логику
        # если поставка в статусе "Ожидается"

        # TODO: добавить бизнес логику для проверки поставки по статусу и влага "Ожидается" (is_wait_confirm)
        if supply.is_wait_confirm:
            raise BadRequestError("Cannot change status - supply is wait confirm")
        elif supply.status == CancelledAssembleStatus.cancelled:
            raise BadRequestError("Cannot change status - supply is cancelled")
        if supply.status == StatusForUpdate.adopted:
            raise BadRequestError("Cannot change status - supply is adopted")

        supply.status = status.status
        supply = await self._update_supply_by_supplier_id_and_flush_session(
            supplier_id=supplier_id,
            supply=supply
        )

        # переместить в отдельную бизнес логигику проверку статуса
        if status.status == StatusForUpdate.adopted:
            await self._create_expenses_company_by_supply(supply)

        return supply


    async def _create_expenses_company_by_supply(self, supply: SupplyItem) -> Iterable[ExpenseCompanyItem]:
        """Создать расходы компании на поставку"""
        supply_products: Iterable[SupplyProductItem] = await self._get_supply_products_by_supply(supply)
        expenses = await self._create_all_expenses_company_and_flush_session(
            adding_expense_service=AddingExpenseCompany(self.session),
            supply=supply,
            supply_products=supply_products
        )
        return expenses


    async def _get_supply_products_by_supply(self, supply: SupplyItem) -> Iterable[SupplyProductItem]:
        """Извлечь продукты в поставке из поставки"""
        supply_products: Iterable[SupplyProductItem] = await self.supply_product_repo.get_by_supply_id(supply.id)
        if not supply_products:
            raise NotFoundError("not found products")
        return supply_products

    async def _create_all_expenses_company_and_flush_session(
            self,
            adding_expense_service: AddingExpenseCompany,
            supply: SupplyItem,
            supply_products: Iterable[SupplyProductItem]
    ) -> Iterable[ExpenseCompanyItem]:
        """Создать расходы компании на поставку и зафиксировать изменения в сессии"""
        expenses_list = []
        for supply_product in supply_products:
            expense_item = ExpenseCompanyItem(
                company_id=supply.company_id,
                product_version_id=supply_product.product_version_id,
                quantity=supply_product.quantity
            )
            expense = await adding_expense_service.adding_expense_process(expense_item)
            expenses_list.append(expense)
            await self.session.flush()
        return expenses_list

    
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
        supply_products: Optional[List[SupplyProductItem]] = await self.supply_product_repo.get_by_supply_id(
            supply_id=supply.id
        )
        if supply_products is None:
            raise NotFoundError("Supplies products is not in supply")
        product_service = ProductService(self.session)
        # Вынести получение продукта по продукту в поставке в цикл
        # products: Iterable[ProductItem] = await product_service.get_products_by_supplies_products(
        #     supplies_products=supply_products
        # )
        # products_ids = [p.id for p in products]

        expenses_list = list()
        expense_service = ExpenseSupplierService(self.session)

        for supply_product in supply_products:
            product = await product_service.get_product_by_product_version_id(
                product_version_id=supply_product.product_version_id
            )
            expense = await expense_service.get_expense_by_id_supplier_and_product(
                supplier_id=supplier_id,
                product_id=product.id
            )

            expense.reserved -= supply_product.quantity
            if status.status == CancelledAssembleStatus.assemble:
                expense.quantity -= supply_product.quantity

            expense_update = await expense_service.update_expense(expense)
            expenses_list.append(expense_update)

        return expenses_list
    

    async def delete_supply(
            self, 
            supply_id: int,
    ) -> None:
        """Удалить поставку"""
        supply = await self.supply_repo.get_by_id(supply_id)
        if not supply:
            raise NotFoundError("not found supply")
        await self.supply_repo.delete(supply.id)
        await self.session.flush()
        return
