from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from core import settings
from core.db import db_core

#from app.schema.expenses


router = APIRouter(
    tags=settings.api.expenses.tags,
    prefix=settings.api.expenses.prefix,
)


@router.get("/expenses")
async def get_expenses(
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass

@router.post("/expenses", status_code=201)
async def add_expense(
#    expense_data: ExpenseRequest, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass


@router.patch("/expenses/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: int,
#   expense_quantity: ExpenseQuantity
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass


@router.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass
