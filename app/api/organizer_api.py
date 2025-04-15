from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from core.db import db_core

from core import settings

from schemas.organizer import (
    OrganizerRegisterRequest,
    OrganizersResponse,
)

from service.busines_service import OrganizerService, UserService

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
    try:
        id = request.state.user_id

        organizer_service = OrganizerService(session=session)
        organizer = await organizer_service.register_company_with_admin(
            name=data.name,
            address=data.address,
            inn=data.inn,
            bank_details=data.bank_details,
            role=data.role,
            id=id
        )
        await session.flush()

        # регистрация администратора
        user_service = UserService(session=session)
        admin = await user_service.assign_admin_to_company(
            user_id=id,
            organizer_id=organizer.id,
        )
        await session.flush()
    except Exception as e:
        await session.rollback()
        print(f"ORGANIZER\n{e}")
    
    await session.commit()

    return {"details": "OK"}

