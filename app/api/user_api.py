from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends, 
    status,
    Query,
    HTTPException
)
from core.db import db_core

from api.dependencies import check_is_admin

from core import settings
from service.bussines_services.user import UserService
from schemas.user import (
    UserCompanySchema,
    UserSchema
)
from service.redis_service import UserDataRedis, redis_user
from logger import logger

router = APIRouter(
    prefix=settings.api.users.prefix,
    tags=settings.api.users.tags,
)


# @router.get("/{user_id}", response_model=UserSchema)
# async def get_user(
#     user_id: int,
#     session: AsyncSession = Depends(db_core.session_getter)
# ):
#     """Получить пользователя по id"""
#     user_service = UserService(session=session)
#     user_response = await user_service.get_user_by_id(user_id=user_id)
#     return UserSchema(**user_response)


# @router.put("/{user_id}", response_model=UserSchema)
# async def update_user(
#     user_id: int,
#     data: UserSchema,
#     session: AsyncSession = Depends(db_core.session_getter)
# ):
#     """Обновить пользователя по id"""
#     user_service = UserService(session=session)
#     user_item = user_service.update_user(
#         content=UserItem(**data.model_dump())
#     )
#     return UserSchema(**user_item)


@router.get("/company", response_model=UserSchema)
async def get_user_company(
    link_code: Optional[int] = Query(None), 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить пользователя по пригласительному коду"""
    user_service = UserService(session=session)
    user = await user_service.get_user_by_link_code(
        link_code=link_code
    )
    return UserSchema(id=user.id, **user.dict)


@router.post("/company", status_code=status.HTTP_201_CREATED)
async def add_user_to_company(
    data: UserCompanySchema,
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Создать учетную запись пользователя в компании"""
    try:
        user_service = UserService(session=session)
        user_company = await user_service.assign_user_to_company(
            user_data=user_data,
            user_to_company_id=data.id,
            role=data.role
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating user company\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    await session.commit()
    # установка только что созданной уч. 
    # записи пользователя в компании в redis
    try:
        await user_service.set_data_user_to_redis(
            user_id=user_company.id,
            user_context=UserDataRedis(
                user_company_id=user_company.id,
                user_company_role=user_company.role,
                organizer_id=user_company.organizer_id,
                organizer_role=user_data.organizer_role
            )
        )
    except Exception as e:
        logger.error(
            msg="Error set user data in Redis\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"detail": "OK"}


@router.delete("/company", status_code=204)
async def remove_user_from_company(
    user_id: Optional[int] = Query(None),
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удалить учетную запись пользователя из компании"""
    try:
        user_service = UserService(session=session)
        await user_service.remove_user_from_company(
            user_data=user_data,
            user_for_remove_id=user_id
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error removing user company\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    await session.commit()
    
    try:
        await redis_user.delete_data(user_id)
    except Exception as e:
        pass
        logger.error(
            msg="Error set user data in Redis\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return {"detail": "OK"}
