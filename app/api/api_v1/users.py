from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import UserRead


# создание роутера для api пользователя, импорт настроек префикса и тегов
router = APIRouter(
    prefix=settings.api.v1.users,
    tags=settings.api.v1.tags
)


@router.get("", response_model=list[UserRead])
async def get_user(
    session: AsyncSession = Depends(db_core.session_getter)
):
    # crud операции с аргументов session
    pass