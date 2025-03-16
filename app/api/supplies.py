from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from core.db import db_core

from core import settings

router = APIRouter(
    prefix=settings.api.v1.supplies_prefix,
    tags=settings.api.v1.supplies_tags
)


@router.get("")
async def get_supplies(session: AsyncSession = Depends(db_core.session_getter)):
    """Получить список всех поставок"""
    pass


@router.post("")
async def create_supply(session: AsyncSession = Depends(db_core.session_getter)):
    """Создать новую поставку"""
    pass

