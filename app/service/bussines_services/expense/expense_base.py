from sqlalchemy.ext.asyncio import AsyncSession

from abc import ABC, abstractmethod
from typing import List

from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseSupplierItem,
    ExpenseCompanyItem,
    ExpenseUpdateQuantityItem
)


class ExpenseInterface(ABC):
    """Интерфейс для работы с расходами"""
    def __init__(self, session: AsyncSession):
        self.session = session
    
    @abstractmethod
    async def get_expenses_by_organizer(self, organizer_id: int) -> List[ExpenseWithInfoProductItem]:
        """Получить все расходы"""
        pass
    
    @abstractmethod
    async def get_expense(
        self, 
        expense_id: int,
        organizer_id: int
    ) -> ExpenseWithInfoProductItem:
        """Получить подробную информацию о расходе"""
        pass
    
    @abstractmethod
    async def update_quantity_expense(
        self, 
        expense_update_quantity: ExpenseUpdateQuantityItem
    ) -> ExpenseCompanyItem | ExpenseSupplierItem: # Указать TypeVar
        """Обновить количество расхода"""
        pass
    
    @abstractmethod
    async def delete_expense(self, expense_id: int) -> ExpenseSupplierItem:
        """Удалить расход"""
        pass
    