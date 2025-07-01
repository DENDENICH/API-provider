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
from service.items_services.supply import SupplyCreateItem, SupplyStatus
from service.bussines_services.supply import SupplyService

from schemas.supply import (
    SupplyCreateRequest,
    SuppliesCancelledAssembleStatus,
    SupplyStatusUpdate
)

from logger import logger

from exceptions.exceptions import NotFoundError, BadRequestError


router = APIRouter(
    prefix=settings.api.supplies.prefix,
    tags=settings.api.supplies.tags,
)


@router.get("") #response_model=SuppliesResponse)
async def get_supplies(
    is_wait_confirm: bool = Query(False),
    limit: int = Query(100),
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить список всех поставок"""
    try:
        supply_service = SupplyService(session=session)
        supplies = await supply_service.get_all_supplies_by_user_data(
            limit=limit,
            user_data=user_data,
            is_wait_confirm=is_wait_confirm,
        )

    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Supply is not found \n{}".format(user_data.organizer_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error getting supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

                
    return {"supplies": [supply.dict for supply in supplies]}


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
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Supply is not found \n{}".format(user_data.organizer_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
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
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Supply is not found \n{}".format(user_data.organizer_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error update supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    await session.commit()
    return {"details": "No content"}


@router.patch("/{supply_id}/status", status_code=status.HTTP_204_NO_CONTENT)
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
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Supply is not found \n{}".format(user_data.organizer_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error update supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    await session.commit()
    return {"details": "No content"}

# Сделано на случай багов с поставками
@router.delete("/{supply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supply(
    supply_id: int,
    # user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удалить поставку"""
    try:
        supply_service = SupplyService(session=session)
        await supply_service.delete_supply(
            supply_id=supply_id
        )
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Supply is not found \n{}".format(supply_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error delete supply\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    await session.commit()
    return {"details": "No content"}
