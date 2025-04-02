from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import UserRead

from utils.jwt_process import jwt_processes


# создание роутера для api пользователя, импорт настроек префикса и тегов
router = APIRouter(
    prefix=settings.api.auth.prefix,
    tags=settings.api.auth.tags
)


@router.post(
        "/registry", 
        status_code=status.HTTP_201_CREATED
)
async def registry(
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Restry user"""
    pass


@router.post(
        "/login",
        status_code=status.HTTP_200_OK
)
async def login(
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Login user"""
    pass
