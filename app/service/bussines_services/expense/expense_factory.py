from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum

from .expense_company import ExpenseCompanyService
from .expense_supplier import ExpenseSupplierService
from .expense_base import ExpenseInterface


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


class ExpenseFactory:
    """Фабрика для создания экземпляров класса для работы с расходами"""

    @classmethod
    def make_expense_service(
        cls, 
        session: AsyncSession, 
        organizer_role: str
    ) -> ExpenseInterface:
        """Создать экземпляр класса для работы с расходами"""
        if organizer_role == OrganizerRole.company:
            return ExpenseCompanyService(session=session)
        elif organizer_role == OrganizerRole.supplier:
            return ExpenseSupplierService(session=session)
        else:
            # TODO: исправить на пользовательскую ошибку
            raise ValueError(f"Unknown organizer role: {organizer_role}")
        