from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends, 
    status,
    Query,
    Request,
    HTTPException
)
from core.db import db_core

from core import settings
from service.bussines_services.user import UserService
from schemas.user import (
    UserCompanySchema,
    UserSchema
)
from service.redis_service import UserContext, redis
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
    request: Request,
    link_code: Optional[int] = Query(None), 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получить пользователя по пригласительному коду"""
    user_service = UserService(session=session)
    user = await user_service.get_user_by_link_code(
        link_code=link_code,
        id=request.state.user_id
    )
    return UserSchema(id=user.id, **user.dict)


@router.post("/company", status_code=status.HTTP_201_CREATED)
async def add_user_to_company(
    request: Request,
    data: UserCompanySchema,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Создать учетную запись пользователя в компании"""
    try:
        id = request.state.user_id
        user_service = UserService(session=session)
        user_company = await user_service.assign_user_to_company(
            id=id,
            user_id=data.id,
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
    # установка пользовательских данных в redis
    try:
        admin_data = await redis.get_user_data(user_id=id)
        await user_service.set_data_user_to_redis(
            user_id=user_company.id,
            user_context=UserContext(
                user_company_id=user_company.id,
                user_company_role=user_company.role,
                organizer_id=user_company.organizer_id,
                organizer_role=admin_data["user_company_role"]
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
    return {"detail": "OK"}


@router.delete("/company", status_code=204)
async def remove_user_from_company(
    request: Request,
    user_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Удалить учетную запись пользователя из компании"""
    try:
        user_service = UserService(session=session)
        await user_service.remove_user_from_company(
            id=request.state.user_id,
            user_id=user_id
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
    
    # удаление свойств о уч. записи в компании, обновление данных
    try:
        user_context = await redis.get_user_data(user_id=user_id)
        if user_context:
            await redis.set_user_data(
                user_id=user_id,
                data=UserContext(
                    user_company_id=None,
                    user_company_role=None,
                    organizer_id=user_context["organizer_id"],
                    organizer_role=user_context["organizer_role"]
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

    return {"detail": "OK"}
