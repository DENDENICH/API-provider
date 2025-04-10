from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from core.db import db_core

from core import settings

from schemas.organizer import (
    OrganizerRegisterRequest,
    OrganizersResponse,
)

from service.busines_service import OrganizerService

router = APIRouter(
    prefix=settings.api.organizers.prefix,
    tags=settings.api.organizers.tags,
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_organizer(
    request: Request,
    data: OrganizerRegisterRequest, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Регистрация организации"""
    organizer_service = OrganizerService(session=session)
    organizer = await organizer_service.register_company_with_admin(
        name=data.name,
        address=data.address,
        inn=data.inn,
        bank_details=data.bank_details,
        user_id=request.state.user_id
    )
    await session.commit()

    return {"details": "OK"}

