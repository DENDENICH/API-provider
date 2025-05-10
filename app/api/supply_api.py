from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from core.db import db_core

from core import settings

from api.dependencies import (
    get_user_from_redis, 
    check_is_supplier, 
    check_is_company
)

from service.redis_service import UserDataRedis
from app.service.items_services.supply import SupplyCreateItem, SupplyStatus
from service.bussines_services.supply import SupplyService

from schemas.supply import (
    SuppliesResponse,
    SupplyCreateRequest,
    SuppliesCancelledAssembleStatus,
    SupplyStatusUpdate,
    SupplyProductCreate
)

from logger import logger

from exceptions import ReverseAmountError


router = APIRouter(
    prefix=settings.api.supplies.prefix,
    tags=settings.api.supplies.tags,
)


@router.get("", response_model=SuppliesResponse)
async def get_supplies(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить список всех поставок"""
    try:
        supply_service = SupplyService(session=session)
        supplies = await supply_service.get_all_supplies_by_user_data(
            user_data=user_data
        )
            
        return SuppliesResponse(
            supplies=[supply.dict for supply in supplies]
        )
    except Exception as e:
        logger.error(
            msg="Error getting supplies\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create_supply(
    supply: SupplyCreateRequest,
    user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Создать новую поставку"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.check_is_contract_exist(
            company_id=user_data.organizer_id,
            supplier_id=supply.supplier_id
        )
        await supply_service.create_supply(
            supply=SupplyCreateItem.get_supply_create_item_by_schema_and_company_id(
                schema=supply,
                company_id=user_data.organizer_id
            )
        )
    except ReverseAmountError as e:
        session.rollback()
        logger.error(
            msg="Error creating supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Oversupply of reserves"
        )
    
    except Exception as e:
        session.rollback()
        logger.error(
            msg="Error creating supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    return {"details": "No content"}
    


@router.get("/{supply_id}")
async def assemble_or_cancel_supply(
    supply_id: int,
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить информацию о поставке"""
    pass


@router.patch("/{supply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assemble_or_cancel_supply(
    supply_id: int,
    status: SuppliesCancelledAssembleStatus,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Принять или отклонить поставку"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.assemble_or_cancel_supply(
            status=SupplyStatus(
                id=supply_id,
                status=status.status
            ),
            supplier_id=user_data.organizer_id
        )
        return {"details": "No content"}
    except Exception as e:
        session.rollback()
        logger.error(
            msg="Error assembling or cancelling supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.patch("/{supply_id}/status", status_code=status.HTTP_201_CREATED)
async def update_status(
    supply_id: int,
    status: SupplyStatusUpdate,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Изменить статус поставки"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.update_supply_status(
            status=SupplyStatus(
                id=supply_id,
                status=status.status
            ),
            supplier_id=user_data.organizer_id
        )
        return {"details": "No content"}
    except Exception as e:
        session.rollback()
        logger.error(
            msg="Error updating supply status\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
