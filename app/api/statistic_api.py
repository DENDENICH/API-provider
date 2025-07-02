from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends, 
    status,
)

from api.dependencies import (
    get_user_from_redis,
    get_session
)

from core import settings
from schemas.dashboard import (
    StatisticCompany,
    StatisticSupplier
)
from service.redis_service import UserDataRedis
from service.bussines_services.dashboard import StaticticService


router = APIRouter(
    prefix=settings.api.dashboard.prefix,
    tags=settings.api.dashboard.tags,
)

@router.get("/company", response_model=StatisticCompany, status_code=status.HTTP_200_OK)
async def get_company_statistic(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(get_session)
):
    """Get statistic dashboard for company"""
    statistic_service = StaticticService(session)
    result: dict = await statistic_service.get_statistics_by_company(
        organizer=user_data
    )
    return StatisticCompany(**result)


@router.get("/supplier", status_code=status.HTTP_200_OK, response_model=StatisticSupplier)
async def get_supplier_statistic(
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(get_session)
):
    """Get statistic dashboard for supplier"""
    statistic_service = StaticticService(session)
    result: dict = await statistic_service.get_statistics_by_supplier(
        organizer=user_data
    )
    return StatisticSupplier(**result)
