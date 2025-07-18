from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends, 
    Query, 
    status
)

from core import settings

from api.dependencies import (
    get_user_from_redis,
    get_session, 
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


router = APIRouter(
    prefix=settings.api.supplies.prefix,
    tags=settings.api.supplies.tags,
)


@router.get("") #response_model=SuppliesResponse)
async def get_supplies(
    is_wait_confirm: bool = Query(False),
    limit: int = Query(100),
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(get_session)
):
    """Get list all supplies"""
    supply_service = SupplyService(session=session)
    supplies = await supply_service.get_all_supplies_by_user_data(
        limit=limit,
        user_data=user_data,
        is_wait_confirm=is_wait_confirm,
    )
         
    return {"supplies": [supply.dict for supply in supplies]}


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create_supply(
    supply: SupplyCreateRequest,
    user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(get_session)
):
    """Create new supply"""
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

    await session.commit()
    return {"details": "No content"}


@router.patch("/{supply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assemble_or_cancel_supply(
    supply_id: int,
    status_data: SuppliesCancelledAssembleStatus,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(get_session)
):
    """Adopted/cancelled supply"""
    supply_service = SupplyService(session=session)
    await supply_service.assemble_or_cancel_supply(
        status=SupplyStatus(
            id=supply_id,
            status=status_data.status
        ),
        supplier_id=user_data.organizer_id
    )
    
    await session.commit()
    return {"details": "No content"}


@router.patch("/{supply_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_status(
    supply_id: int,
    status_data: SupplyStatusUpdate,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(get_session)
):
    """Change status supply"""
    supply_service = SupplyService(session=session)
    await supply_service.update_supply_status(
        status=SupplyStatus(
            id=supply_id,
            status=status_data.status
        ),
        supplier_id=user_data.organizer_id
    )
    
    await session.commit()
    return {"details": "No content"}
