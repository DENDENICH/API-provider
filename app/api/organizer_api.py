from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status, HTTPException
from core.db import db_core

from core import settings

from schemas.organizer import (
    OrganizerRegisterRequest,
    OrganizerResponse
)

from service.bussines_services.user import UserService
from service.bussines_services.organizer import OrganizerService
from service.redis_service import UserDataRedis

from exceptions.exceptions import NotFoundError, BadRequestError

from logger import logger

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
    except NotFoundError as e:
        await session.rollback()
        logger.error(
            msg="Error creating organizer\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    except BadRequestError as e:
        await session.rollback()
        logger.error(
            msg="Error creating organizer\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating organizer\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # установка пользовательских данных в redis
    try:
        await user_service.set_data_user_to_redis(
            user_id=id,
            user_context=UserDataRedis(
                user_id=admin.id,
                user_company_id=admin.id,
                user_company_role=admin.role,
                organizer_id=organizer.id,
                organizer_role=organizer.role
            )
        )
    except Exception as e:
        pass
        logger.error(
            msg="Error set user data in Redis\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    await session.commit()

    return OrganizerResponse(id=organizer.id, **organizer.dict)

