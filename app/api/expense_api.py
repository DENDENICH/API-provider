from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from core import settings
from core.db import db_core

from schemas.expense import (
    ExpenseQuantity, 
    ExpenseResponse,
    ExpensesResponse
)

from service.bussines_services.expense.expense_factory import ExpenseFactory
# from api.dependencies import 


router = APIRouter(
    tags=settings.api.expenses.tags,
    prefix=settings.api.expenses.prefix,
)


@router.get("/expenses", response_model=ExpensesResponse)
async def get_expenses(
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить все расходы"""
    pass


@router.patch("/expenses/{expense_id}", status_code=204, response_model=ExpenseResponse)
async def update_quantity_expense(
    expense_id: int,
    expense_quantity: ExpenseQuantity,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Изменить количество расхода"""
    pass


@router.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удалить расход"""
    pass
