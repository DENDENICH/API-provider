from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status
from core.db import db_core

from core import settings

from schemas.organizer import (
    OrganizerRegisterRequest,
    OrganizersResponse
)

router = APIRouter(
    prefix=settings.api.organizers.prefix,
    tags=settings.api.organizers.tags,
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_organizer(
    data: OrganizerRegisterRequest, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Регистрация организации"""
    await session.commit()


@router.get("", response_model=OrganizersResponse)
async def get_organizers(session: AsyncSession = Depends(db_core.session_getter)):
    """Получение организации"""
    pass