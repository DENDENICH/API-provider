from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthTokenSchema
)

from auth.utils.jwt_processes import jwt_processes as jwt

from auth.service.user_auth import UserAuthService


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
    user_service = UserAuthService(session=session)

    user_item = await user_service.register_user(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=user.password
    )

    token = user_service.get_jwt(user=user_item)
    # ссылка для перенаправления пользователя
    next_route = "/organizer/register" if user.user_type == "admin" else "/"
    token["next_route"] = next_route

    # коммит всех изменений в БД
    await session.commit()
    
    return AuthTokenSchema(**token)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthTokenSchema)
async def login(
    user: UserLoginRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Вход пользователя"""
    user_service = UserAuthService(session=session)

    user_item = await user_service.check_login_user(
        email=user.email,
        password=user.password
    )

    token = user_service.get_jwt(user=user_item)
    return AuthTokenSchema(**token)
