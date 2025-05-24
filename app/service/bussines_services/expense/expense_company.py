from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from service.repositories import (
    ExpenseCompanyRepository,
)
from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseCompanyItem,
    ExpenseUpdateQuantityItem
)
from .expense_base import ExpenseInterface
from exceptions import NotFoundError


class ExpenseCompanyService(ExpenseInterface):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)
        self.expense_repo = ExpenseCompanyRepository(session=session)

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
    ) -> ExpenseCompanyItem:
        """Получить расход по id расхода и организатора"""
        expense = await self.expense_repo.get_by_expense_and_company_id(
            expense_id=expense_id,
            company_id=organizer_id
        )
        if not expense:
            raise NotFoundError("Expense not found")
        return expense

    async def add_expense(self, expense: ExpenseCompanyItem) -> ExpenseCompanyItem:
        """Добавить новый расход"""
        expense_item = await self.expense_repo.create(expense)
        if not expense_item:
            return None
        return expense_item

    async def update_quantity_expense(
        self, 
        expense_update_quantity: ExpenseUpdateQuantityItem
    ) -> ExpenseCompanyItem:
        """Обновить количество расхода"""
        expense = await self.get_expense(
            expense_id=expense_update_quantity.expense_id,
            organizer_id=expense_update_quantity.organizer_id
        )
        if not expense:
            raise NotFoundError("Expenses not found")
        
        expense.quantity = expense_update_quantity.quantity
        expense_update = await self.expense_repo.update(expense)

        return expense_update
    
    async def delete_expense(self, expense_id: int) -> ExpenseCompanyItem:
        """Удалить расход"""
        #TODO: Сделать также и удаление продукта 
        return await self.expense_repo.delete(expense_id)
