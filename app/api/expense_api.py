from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core import settings
from core.db import db_core

from api.dependencies import get_user_from_redis, OrganizerRole

from schemas.expense import (
    ExpenseQuantity,
    ExpenseResponse,
    ExpensesResponse
)

from service.bussines_services.expense.expense_factory import ExpenseFactory
from service.bussines_services.expense.expense_base import ExpenseInterface
from service.items_services.expense import (
    ExpenseUpdateQuantityItem,
    ExpenseWithInfoProductItem,
    ExpenseSupplierItem
)
from service.bussines_services.product import ProductService
from service.redis_service import UserDataRedis

from exceptions.exceptions import NotFoundError, BadRequestError

from logger import logger


router = APIRouter(
    tags=settings.api.expenses.tags,
    prefix=settings.api.expenses.prefix,
)


@router.get("", response_model=ExpensesResponse)
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
        
    except NotFoundError as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    except BadRequestError as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return ExpensesResponse(
            expenses=[expense.dict for expense in expenses]
        )


@router.get("/{expenses_id}", response_model=ExpenseResponse)
async def get_expense_by_id(
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
    except NotFoundError as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    except BadRequestError as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error getting expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return ExpenseResponse(**expense.dict)


@router.patch("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    except NotFoundError as e:
        await session.rollback()
        logger.error(
            msg="Error updating sttaus expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    except BadRequestError as e:
        await session.rollback()
        logger.error(
            msg="Error updating status expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error updating sttaus expenses\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    await session.commit()
    return {"detail": "No content"}


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
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
        expense: ExpenseSupplierItem = await expense_service.delete_expense(
            expense_id=expense_id
        )

        # убрать данный костыль из endpoint
        if user_data.organizer_role == OrganizerRole.supplier:
            product_service = ProductService(session=session)
            await product_service.delete_product(product_id=expense.product_id)
            
    except NotFoundError as e:
        await session.rollback()
        logger.error(
            msg="Error deleting expense\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    except BadRequestError as e:
        await session.rollback()
        logger.error(
            msg="Error deleting expense\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error deleting expense\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    await session.commit()
    return {"detail": "No content"}

