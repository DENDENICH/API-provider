from sqlalchemy.ext.asyncio import AsyncSession

from enum import Enum
from fastapi import Request, Depends

from service.redis_service import redis_user, UserDataRedis 

<<<<<<< HEAD
from exceptions import forbiden_error
=======
from exceptions.exceptions import ForbidenError
>>>>>>> exception-working


class UserRoleType(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee" 

class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


def get_session(request: Request) -> AsyncSession:
    """Получить объект сессии из запроса"""
    return request.state.session


async def get_user_from_redis(request: Request) -> UserDataRedis:
    user_id = request.state.user_id
    if (user_data := await redis_user.get_data(user_id)) is None:
        raise ForbidenError("You don't have permission to access")
    user_data.user_id = user_id
    return user_data

async def check_is_admin(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.user_company_role != UserRoleType.admin:
        raise ForbidenError("You don't have permission to access")
    return user_data

async def check_is_supplier(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.organizer_role != OrganizerRole.supplier:
        raise ForbidenError("You don't have permission to access")
    return user_data

async def check_is_company(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.organizer_role != OrganizerRole.company:
        raise ForbidenError("You don't have permission to access")
    return user_data
