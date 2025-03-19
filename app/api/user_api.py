from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import UserRead

from utils.jwt_process import jwt_processes

# создание роутера для api пользователя, импорт настроек префикса и тегов
router = APIRouter(
    prefix=settings.api.users.prefix,
    tags=settings.api.users.tags
)


@router.post("/login")
async def login(
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass