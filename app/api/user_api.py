from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    status,
    Query,
    Depends 
)

from api.dependencies import (
    check_is_admin,
    get_session
)

from core import settings
from service.bussines_services.user import UserService
from schemas.user import (
    UserCompanySchema,
    UsersCompanyWithUserSchema,
    UserCompanyWithUserSchema
)
from service.redis_service import UserDataRedis, redis_user


router = APIRouter(
    prefix=settings.api.users.prefix,
    tags=settings.api.users.tags,
)


@router.get(
    "/company", 
    status_code=status.HTTP_200_OK, 
    response_model=UsersCompanyWithUserSchema
)
async def get_all_employee(
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
<<<<<<< HEAD
    """Получить все учетые записи пользователей в компании"""
    try:
        user_service = UserService(session=session)
        users_company = await user_service.get_all_employ_by_organizer_id(
            organizer_id=user_data.organizer_id
        )
        
    except NotFoundError as e:
        logger.info(
            msg="Users is not found by organizer id -> \n{}".format(user_data.organizer_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.error(
            msg="Error creating user\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
=======
    """Get all account user's by organizer"""
    user_service = UserService(session=session)
    users_company = await user_service.get_all_employ_by_organizer_id(
        organizer_id=user_data.organizer_id
    )
>>>>>>> exception-working

    return UsersCompanyWithUserSchema(
        users=[UserCompanyWithUserSchema(**u.dict) for u in users_company]
    )


@router.post("/company", status_code=status.HTTP_201_CREATED)
async def add_user_to_company(
    data: UserCompanySchema,
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
    """Create account user's in organizer"""
    user_service = UserService(session=session)
    user_company = await user_service.assign_user_to_company_by_link_code(
        user_data=user_data,
        link_code=data.link_code,
        role=data.role
    )
    await session.commit()

    # save user data in redis
    await user_service.set_data_user_to_redis(
        user_id=user_company.id,
        user_context=UserDataRedis(
            user_company_id=user_company.id,
            user_company_role=user_company.role,
            organizer_id=user_company.organizer_id,
            organizer_role=user_data.organizer_role
        )
    )

    return {"detail": "Not content"}


@router.delete("/company", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_company(
    user_id: int = Query(int),
    user_data: UserDataRedis = Depends(check_is_admin),
    session: AsyncSession = Depends(get_session)
):
    """Delete account user's in organizer"""
    user_service = UserService(session=session)
    await user_service.remove_user_from_company(
        user_data=user_data,
        user_for_remove_id=user_id
    )

    await session.commit()
    
    await redis_user.delete_data(user_id)

    return {"detail": "No content"}
