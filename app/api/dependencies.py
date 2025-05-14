from enum import Enum
from fastapi import Request, Depends

from service.redis_service import redis_user, UserDataRedis 

from exceptions import not_found_error, forbiden_error


class UserRoleType(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee" 

class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


async def get_user_from_redis(request: Request) -> UserDataRedis:
    user_id = request.state.user_id
    if (user_data := await redis_user.get_data(user_id)) is None:
        raise not_found_error
    user_data.user_id = user_id
    return user_data

async def check_is_admin(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.user_company_role != UserRoleType.admin:
        raise forbiden_error
    return user_data

async def check_is_supplier(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.organizer_role != OrganizerRole.supplier:
        raise forbiden_error
    return user_data

async def check_is_company(
        user_data: UserDataRedis = Depends(get_user_from_redis)
) -> UserDataRedis:
    if user_data.organizer_role != OrganizerRole.company:
        raise forbiden_error
    return user_data

