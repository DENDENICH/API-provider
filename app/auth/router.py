from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthTokenSchema,
    UserTypeForNextRoute
)

from auth.service.user_auth import UserAuthService

from service.bussines_services.link_code import LinkCodeService
from service.bussines_services.user import UserService
from service.redis_service import UserDataRedis, redis_user

from exceptions import NotFoundError, BadRequestError

from logger import logger


router = APIRouter(
    prefix=settings.api.auth.prefix,
    tags=settings.api.auth.tags
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthTokenSchema)
async def registry(
    data: UserRegisterRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Регистрация пользователя"""
    try:
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
        if data.user_type == UserTypeForNextRoute.organizer:
            next_route = "organizers/register"
        else:
            next_route = "/"
            link_code_service = LinkCodeService(session=session)
            await link_code_service.create_link_code(user_id=user.id)

        token = user_service.get_jwt(user=user)

        # установка пользовательских данных в redis
        await redis_user.set_data(
            key=user.id,
            data=UserDataRedis(user_id=user.id)
        )
    
    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Is not found\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating user\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    await session.commit()
    
    return AuthTokenSchema(next_route=next_route, **token)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthTokenSchema)
async def login(
    data: UserLoginRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Вход пользователя"""
    try:
        user_auth_service = UserAuthService(session=session)
        user = await user_auth_service.check_login_user(
            email=data.email,
            password=data.password
        )
        token = user_auth_service.get_jwt(user=user)

    except NotFoundError as e:
        await session.rollback()
        logger.info(
            msg="Is not found\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        await session.rollback()
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating user\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    # установка пользовательских данных в redis
    try:
        user_service = UserService(session=session)
        await user_service.set_data_user_to_redis(user_id=user.id)
    except Exception as e:
        logger.error(
            msg="Error set user data in Redis\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"

        )
    return AuthTokenSchema(next_route=None, **token)
