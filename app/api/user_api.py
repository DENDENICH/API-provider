from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from core.db import db_core

from core import settings

router = APIRouter(
    prefix=settings.api.users.prefix,
    tags=settings.api.users.tags,
)


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить пользователя по id"""
    pass


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Обновить пользователя по id"""
    pass


@router.get("/user/company")
async def get_user_company(
    add_to_company_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass


@router.post("/user/company", status_code=201)
async def add_user_to_company(
    id: int, 
    role: str, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass


@router.delete("/user/company", status_code=204)
async def remove_user_from_company(
    id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass
