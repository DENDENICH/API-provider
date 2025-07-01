from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends, 
    status,
    HTTPException
)
from core.db import db_core

from api.dependencies import get_user_from_redis

from core import settings
from schemas.dashboard import (
    StatisticCompany,
    StatisticSupplier
)
from service.redis_service import UserDataRedis
from service.bussines_services.dashboard import StaticticService

from exceptions.exceptions import NotFoundError, BadRequestError
from logger import logger

router = APIRouter(
    prefix=settings.api.dashboard.prefix,
    tags=settings.api.dashboard.tags,
)

@router.get("/company", response_model=StatisticCompany, status_code=status.HTTP_200_OK)
async def get_company_statistic(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить полную статистику компании"""
    try:
        statistic_service = StaticticService(session)
        result: dict = await statistic_service.get_statistics_by_company(
            organizer=user_data
        )
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="statisic is not found\n{}".format(e)
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
            msg="Error gettint dashboard\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return StatisticCompany(**result)


@router.get("/supplier", status_code=status.HTTP_200_OK, response_model=StatisticSupplier)
async def get_supplier_statistic(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить полную статистику поставщика"""
    try:
        statistic_service = StaticticService(session)
        result: dict = await statistic_service.get_statistics_by_supplier(
            organizer=user_data
        )
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="statisic is not found\n{}".format(e)
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
            msg="Error gettint dashboard\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return StatisticSupplier(**result)
