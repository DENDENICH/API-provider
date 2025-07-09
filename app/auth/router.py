from fastapi import APIRouter, Depends, status, Request

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings

from schemas.user import UserRegisterRequest, UserLoginRequest

from auth.service.user_auth import UserAuthService

from service.bussines_services.user import UserService
from service.redis_service import UserDataRedis, redis_user

from api.dependencies import get_session


router = APIRouter(
    prefix=settings.api.auth.prefix,
    tags=settings.api.auth.tags
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def registry(
    request: Request,
    data: UserRegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    """Регистрация пользователя"""
    user_service = UserAuthService(session=session)

    # регистрация пользователя
    user = await user_service.register_user(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password=data.password
    )
    # отправляем транзакцию, но не фиксируем
    await session.flush()

    # создание пригласительного кода если запрос на регистрацию от сотрудника
    # if data.user_type == UserTypeForNextRoute.organizer:
    #     next_route = "organizers/register"
    # else:
    #     next_route = "/"
    #     link_code_service = LinkCodeService(session=session)
    #     await link_code_service.create_link_code(user_id=user.id)

    # установка пользовательских данных в redis
    await redis_user.set_data(
        key=user.id,
        data=UserDataRedis(user_id=user.id)
    )

    await session.commit()

    request.state.user_id = user.id
    

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    data: UserLoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """Вход пользователя"""
    user_auth_service = UserAuthService(session=session)
    user = await user_auth_service.check_login_user(
        email=data.email,
        password=data.password
    )


    # установка пользовательских данных в redis
    user_service = UserService(session=session)
    user_context = await user_service.set_data_user_to_redis(user_id=user.id)

    request.state.user_id = user.id
