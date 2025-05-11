from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Query, status
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
    is_wait_confirm: bool = Query(None),
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить список всех поставок"""
    try:
        supply_service = SupplyService(session=session)
        supplies = await supply_service.get_all_supplies_by_user_data(
            user_data=user_data
        )

    except Exception as e:
        logger.error(
            msg="Error getting supplies\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
                
    return SuppliesResponse(
        supplies=[supply.dict for supply in supplies]
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
    await session.commit()
    return {"details": "No content"}


@router.patch("/{supply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assemble_or_cancel_supply(
    supply_id: int,
    status_data: SuppliesCancelledAssembleStatus,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Принять или отклонить поставку"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.assemble_or_cancel_supply(
            status=SupplyStatus(
                id=supply_id,
                status=status_data.status
            ),
            supplier_id=user_data.organizer_id
        )
    except Exception as e:
        session.rollback()
        logger.error(
            msg="Error assembling or cancelling supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    await session.commit()
    return {"details": "No content"}


@router.patch("/{supply_id}/status", status_code=status.HTTP_201_CREATED)
async def update_status(
    supply_id: int,
    status_data: SupplyStatusUpdate,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Изменить статус поставки"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.update_supply_status(
            status=SupplyStatus(
                id=supply_id,
                status=status_data.status
            ),
            supplier_id=user_data.organizer_id
        )
    except Exception as e:
        session.rollback()
        logger.error(
            msg="Error updating supply status\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    await session.commit()
    return {"details": "No content"}
