from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from core import settings
from core.db import db_core


router = APIRouter(
    tags=settings.api.suppliers.tags,
    prefix=settings.api.suppliers.prefix,
)


@router.get("") #response_model=SuppliersResponse)
async def get_suppliers(
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить всех поставщиков компании"""
    pass


@router.post("/{supplier_id}", status_code=201)
async def add_supplier(
#    supplier_data: SupplierRequest, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Создать нового поставщика для компании"""
    pass


@router.delete("/{supplier_id}", status_code=204)
async def delete_supplier(
    supplier_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удаление поставщика из контактов"""
    pass
