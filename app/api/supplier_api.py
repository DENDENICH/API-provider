from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import (
    APIRouter,
    Depends, 
    status
)

from schemas.supplier import SuppliersResponse
from schemas.organizer import OrganizerResponse

from core import settings

from api.dependencies import (
    check_is_admin,
    get_session
)

from service.items_services.organizer import OrganizerItem
from service.items_services.contract import ContractItem

from service.bussines_services.organizer import OrganizerService
from service.bussines_services.supplier import SupplierService

from service.redis_service import UserDataRedis


router = APIRouter(
    tags=settings.api.suppliers.tags,
    prefix=settings.api.suppliers.prefix,
)


@router.get("", response_model=SuppliersResponse)
async def get_suppliers(
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
    """Get suppliers by company"""
    supplier_service = SupplierService(session=session)
    suppliers: List[OrganizerItem] = await supplier_service.get_supplier_available_company(
        company_id=user_data.organizer_id
    )

    return SuppliersResponse(
        organizers=[OrganizerResponse(id=supplier.id, **supplier.dict) for supplier in suppliers]
    )
    

@router.get("/{supplier_inn}", response_model=OrganizerResponse)
async def get_supplier_by_inn(
    supplier_inn: int,
    user_data: UserDataRedis = Depends(check_is_admin), 
    session: AsyncSession = Depends(get_session)
):
    """Get supplier by inn"""
    organizer_service = OrganizerService(session=session)
    supplier: OrganizerItem = await organizer_service.get_supplier_by_inn(
        supplier_inn=supplier_inn
    )

    return OrganizerResponse(id=supplier.id, **supplier.dict)


@router.post("/{supplier_id}", status_code=status.HTTP_201_CREATED)
async def add_supplier(
    supplier_id: int, 
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
    """Create new supplier and contract for company"""
    supplier_service = SupplierService(session=session)
    supplier: ContractItem = await supplier_service.create_contract(
        contract_item=ContractItem(
            supplier_id=supplier_id,
            company_id=user_data.organizer_id
        )
    )

    await session.commit()
    return {"detail": "No content"}
    

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
    """Delete supplier by company"""
    supplier_service = SupplierService(session=session)
    await supplier_service.delete_contract(
        supplier_id=supplier_id,
        company_id=user_data.organizer_id
    )
    
    await session.commit()
    return {"detail": "No content"}
