from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Request, 
    Depends, 
    status,
)

from core import settings

from schemas.organizer import (
    OrganizerRegisterRequest,
    OrganizerResponse
)

from service.bussines_services.user import UserService
from service.bussines_services.organizer import OrganizerService
from service.redis_service import UserDataRedis

from api.dependencies import (
    # get_user_from_redis,
    get_session
)


router = APIRouter(
    prefix=settings.api.organizers.prefix,
    tags=settings.api.organizers.tags,
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_organizer(
    request: Request,
    data: OrganizerRegisterRequest, 
    session: AsyncSession = Depends(get_session)
):
    """Регистрация организации"""
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

    # установка пользовательских данных в redis
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
    
    await session.commit()

    return OrganizerResponse(id=organizer.id, **organizer.dict)
