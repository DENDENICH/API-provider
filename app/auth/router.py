from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthTokenSchema,
    UserTypeForNextRoute
)

from auth.utils.jwt_processes import jwt_processes as jwt

from auth.service.user_auth import UserAuthService
from service.bussines_services.link_code import LinkCodeService
from service.bussines_services.user import UserService


router = APIRouter(
    prefix=settings.api.auth.prefix,
    tags=settings.api.auth.tags
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthTokenSchema)
async def registry(
    user: UserRegisterRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Регистрация пользователя"""
    try:
        user_service = UserAuthService(session=session)

        # регистрация пользователя
        user = await user_service.register_user(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=user.password
        )
        # отправляем транзакцию, но не фиксируем
        await session.flush()

        # создание пригласительного кода если запрос на регистрацию от сотрудника
        if user.user_type == UserTypeForNextRoute.organizer:
            next_route = "/organizers/register"
        else:
            next_route = "/"
            link_code_service = LinkCodeService(session=session)
            await link_code_service.create_link_code(user_id=user.id)

        token = user_service.get_jwt(user=user)
        # ссылка для перенаправления пользователя

        # коммит всех изменений в БД
        
    except Exception as e:
        await session.rollback()
        print(e)

    await session.commit()
    
    return AuthTokenSchema(next_route=next_route, **token)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthTokenSchema)
async def login(
    user: UserLoginRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Вход пользователя"""
    user_auth_service = UserAuthService(session=session)

    user = await user_auth_service.check_login_user(
        email=user.email,
        password=user.password
    )
    token = user_auth_service.get_jwt(user=user)

    # установка пользовательских данных в redis
    user_service = UserService(session=session)
    await user_service.set_data_user_to_redis(user.id)

    return AuthTokenSchema(next_route=None, **token)
