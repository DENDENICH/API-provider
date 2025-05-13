from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core import settings
from core.db import db_core

from api.dependencies import get_user_from_redis

from schemas.expense import (
    ExpenseQuantity, 
    ExpenseResponse,
    ExpensesResponse
)

from service.bussines_services.expense.expense_factory import ExpenseFactory
from service.bussines_services.expense.expense_base import ExpenseInterface
from service.items_services.expense import (
    ExpenseUpdateQuantityItem,
    ExpenseWithInfoProductItem
)
from service.redis_service import UserDataRedis

from logger import logger


router = APIRouter(
    tags=settings.api.expenses.tags,
    prefix=settings.api.expenses.prefix,
)


@router.get("/expenses", response_model=ExpensesResponse)
async def get_expenses(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить все расходы"""
    try:
        expense_service: ExpenseInterface = ExpenseFactory.make_expense_service(
            session=session,
            organizer_role=user_data.organizer_role
        )
        expenses: List[ExpenseWithInfoProductItem] = await expense_service.get_expenses_by_organizer(
            organizer_id=user_data.organizer_id
        )
        
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    return ExpensesResponse(
            expenses=[expense.dict for expense in expenses]
        )


@router.get("/expenses/{expenses_id}", response_model=ExpenseResponse)
async def get_expenses(
    expenses_id: int,
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить расход по его id"""
    try:
        expense_service: ExpenseInterface = ExpenseFactory.make_expense_service(
            session=session,
            organizer_role=user_data.organizer_role
        )
        expense = await expense_service.get_expense(
            expense_id=expenses_id,
            organizer_id=user_data.organizer_id
        )
    except Exception as e:
        logger.error(f"Error getting expense by id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    return ExpenseResponse(**expense.dict)


@router.patch("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_quantity_expense(
    expense_id: int,
    expense_quantity: ExpenseQuantity,
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Изменить количество расхода"""
    try:
        expense_service: ExpenseInterface = ExpenseFactory.make_expense_service(
            session=session,
            organizer_role=user_data.organizer_role
        )
        expenses = await expense_service.update_quantity_expense(
            expense_update_quantity=ExpenseUpdateQuantityItem(
                expense_id=expense_id,
                organizer_id=user_data.organizer_id,
                quantity=expense_quantity.quantity
            )
        )
    except Exception as e:
        logger.error(f"Error update quantity expense: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    await session.commit()
    return {"detail": "No content"}


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int, 
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удалить расход"""
    try:
        expense_service: ExpenseInterface = ExpenseFactory.make_expense_service(
            session=session,
            organizer_role=user_data.organizer_role
        )
        expenses = await expense_service.delete_expense(
            expense_id=expense_id
        )
    except Exception as e:
        logger.error(f"Error deleting expense expense: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    await session.commit()
    return {"detail": "No content"}

