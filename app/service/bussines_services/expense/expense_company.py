from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

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
        return await self.expense_repo.create(expense)
        
    
    async def get_expense_by_product_and_organizer_id(
            self,
            product_verison_id: int,
            organizer_id: int
    ) -> Optional[ExpenseCompanyItem]:
        """Получение расхода по id версии продукта и id организации (компании)"""
        return await self.expense_repo.get_by_product_organizer_ids(
            company_id=organizer_id,
            product_version_id=product_verison_id
        )

    async def update_quantity_expense(
        self, 
        expense_update_quantity: ExpenseUpdateQuantityItem
    ) -> ExpenseCompanyItem:
        """Обновить количество расхода"""
        expense_update = await self.expense_repo.update_quantity(expense_update_quantity)
        if not expense_update:
            raise NotFoundError("Expenses not found")

        return expense_update
    
    async def delete_expense(self, expense_id: int) -> ExpenseCompanyItem:
        """Удалить расход"""
        #TODO: Сделать также и удаление продукта 
        if (deleting_expense := await self.expense_repo.delete(expense_id)) is None:
            raise NotFoundError("Expense not found")
        return deleting_expense


class AddingExpenseCompany:
    """Класс для реализации логики добавления товара на склад компании"""
    def __init__(self, session: AsyncSession) -> None:
        self._expense_service = ExpenseCompanyService(session)

    async def adding_expense_process(
        self,
        expense_item: ExpenseCompanyItem
    ) -> ExpenseCompanyItem:
        """Логика добавление продукта на склад компании"""
        if (exists_expense := await self._expense_service.get_expense_by_product_and_organizer_id(
                product_verison_id=expense_item.product_version_id,
                organizer_id=expense_item.company_id
            )
        ) is None:
            return await self._expense_service.add_expense(expense_item)
        else:
            return await self._updating_quantity_exists_expense(
                exists_expense=exists_expense,
                added_quantity=expense_item.quantity
            )
    
    async def _updating_quantity_exists_expense(
            self, 
            exists_expense: ExpenseCompanyItem,
            added_quantity: int
    ) -> ExpenseCompanyItem:
        """Обновление кол-ва существующего продукта на складе"""
        updating_quantity_expense = ExpenseUpdateQuantityItem(
            organizer_id=exists_expense.company_id,
            expense_id=exists_expense.id,
            quantity=exists_expense.quantity + added_quantity
        )
        return await self._expense_service.update_quantity_expense(
            updating_quantity_expense
        )
    