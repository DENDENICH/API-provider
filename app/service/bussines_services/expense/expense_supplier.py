from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from service.repositories import (
    ExpenseSupplierRepository
)
from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseSupplierItem,
    ExpenseAddReservedItem,
    ExpenseUpdateQuantityItem,
)
from .expense_base import ExpenseInterface
from exceptions.exceptions import NotFoundError


class ExpenseSupplierService(ExpenseInterface):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)
        self.expense_repo = ExpenseSupplierRepository(session=session)


    async def get_expenses_by_organizer(self, organizer_id: int) -> List[ExpenseWithInfoProductItem]:
        """Получить все расходы"""
        expenses = await self.expense_repo.get_all_expense_response_items(organizer_id)
        if not expenses:
            raise NotFoundError("Expenses not found")
        return expenses
    

    async def get_expense(
        self, 
        expense_id: int,
        organizer_id: int
    ) -> ExpenseSupplierItem:
        """Получить расход по id"""
        expense = await self.expense_repo.get_by_expense_and_supplier_id(
            expense_id=expense_id,
            supplier_id=organizer_id
        )
        if not expense:
            raise NotFoundError("Expenses not found")
        return expense
    
    
    async def add_expense(self, expense: ExpenseSupplierItem) -> ExpenseSupplierItem:
        """Добавить новый расход"""
        return await self.expense_repo.create(expense)
    

    async def update_quantity_expense(
        self, 
        expense_update_quantity: ExpenseUpdateQuantityItem
    ) -> ExpenseWithInfoProductItem:
        """Обновить количество расхода"""
        expense = await self.get_expense(
            expense_id=expense_update_quantity.expense_id,
            organizer_id=expense_update_quantity.organizer_id
        )
        expense.quantity = expense_update_quantity.quantity
        expense = await self.expense_repo.update(expense)
        if not expense:
            raise NotFoundError("Expenses not found")
        return expense
    

    async def update_expense(self, expense: ExpenseSupplierItem) -> ExpenseSupplierItem:
        """Обновление сущности расхода"""
        expense_update = await self.expense_repo.update(expense)
        if expense_update is None:
            raise NotFoundError("Expenses not found")
        return expense_update
    

    async def get_expense_by_id_supplier_and_product(
            self, 
            supplier_id: int, 
            product_id: int
    ) -> ExpenseSupplierItem:
        """Получить расход по id поставщика и id продукта"""
        expense = await self.expense_repo.get_by_product_and_supplier_id(
            supplier_id=supplier_id,
            product_id=product_id
        )
        if not expense:
            raise NotFoundError("Expenses not found")
        return expense


    async def add_reserved_expense(
        self, 
        add_reverved_expense: ExpenseAddReservedItem
    ) -> ExpenseSupplierItem:
        """Добавить новый резерв расхода"""
        expense: ExpenseSupplierItem = await self.get_expense_by_id_supplier_and_product(
            supplier_id=add_reverved_expense.supplier_id,
            product_id=add_reverved_expense.product_id
        )
        expense.reserved += add_reverved_expense.reserved
        expense = await self.expense_repo.update(expense)
        return expense    


    async def delete_expense(self, expense_id: int) -> ExpenseSupplierItem:
        """Удалить расход"""
        expense: ExpenseSupplierItem = await self.expense_repo.get_by_id(expense_id)
        if not expense:
            raise NotFoundError("Expenses not found")

        expense = await self.expense_repo.delete(expense_id)
        return expense
