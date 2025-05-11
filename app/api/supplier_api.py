from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.supplier import SuppliersResponse
from schemas.organizer import OrganizerResponse

from core import settings
from core.db import db_core

from api.dependencies import check_is_admin

from service.items_services.organizer import OrganizerItem
from service.items_services.contract import ContractItem

from service.bussines_services.organizer import OrganizerService
from service.bussines_services.supplier import SupplierService

from service.redis_service import UserDataRedis

from logger import logger


router = APIRouter(
    tags=settings.api.suppliers.tags,
    prefix=settings.api.suppliers.prefix,
)


@router.get("", response_model=SuppliersResponse)
async def get_suppliers(
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить поставщиков компании"""
    try:
        supplier_service = SupplierService(session=session)
        suppliers: List[OrganizerItem] = await supplier_service.get_supplier_available_company(
            company_id=user_data.organizer_id
        )
    except Exception as e:
        logger.error(f"Error getting suppliers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    return SuppliersResponse(
        suppliers=[supplier.dict for supplier in suppliers]
    )
    

@router.get("/{supplier_inn}", response_model=OrganizerResponse)
async def get_suppliers(
    supplier_inn: int,
    user_data: UserDataRedis = Depends(check_is_admin), 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить поставщика по ИНН"""
    try:
        organizer_service = OrganizerService(session=session)
        supplier: OrganizerItem = await organizer_service.get_supplier_by_inn(
            supplier_inn=supplier_inn
        )
    except Exception as e:
        logger.error(f"Error getting supplier by INN: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    return OrganizerResponse(
        supplier=supplier.dict
    )


@router.post("/{supplier_id}", status_code=201)
async def add_supplier(
    supplier_id: int, 
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Создать нового поставщика для компании"""
    try:
        supplier_service = SupplierService(session=session)
        supplier: ContractItem = await supplier_service.create_contract(
            contract_item=ContractItem(
                supplier_id=supplier_id,
                company_id=user_data.organizer_id
            )
        )
    except Exception as e:
        logger.error(f"Error creating supplier: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    await session.commit()
    return {"detail": "No content"}
    

@router.delete("/{supplier_id}", status_code=204)
async def delete_supplier(
    supplier_id: int,
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удаление поставщика из контактов"""
    try:
        supplier_service = SupplierService(session=session)
        await supplier_service.delete_contract(
            supplier_id=supplier_id,
            company_id=user_data.organizer_id
        )
    except Exception as e:
        logger.error(f"Error deleting supplier: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    await session.commit()
    return {"detail": "No content"}
