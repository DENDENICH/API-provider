from enum import Enum
from fastapi import Request

from service.redis_service import redis_user, UserDataRedis 

from exceptions import not_found_error, forbiden_error


class UserRoleType(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee" 

class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


async def check_is_admin(request: Request) -> UserDataRedis:
    user_id = request.state.user_id
    if (user_data := await redis_user.get_data(user_id)) is None:
        raise not_found_error
    if user_data.user_company_role != UserRoleType.admin:
        raise forbiden_error
    return user_data

async def check_is_supplier(request: Request) -> UserDataRedis:
    user_id = request.state.user_id
    if (user_data := await redis_user.get_data(user_id)) is None:
        raise not_found_error
    if user_data.user_company_role != OrganizerRole.supplier:
        raise forbiden_error
    return user_data

async def check_is_company(request: Request) -> UserDataRedis:
    user_id = request.state.user_id
    if (user_data := await redis_user.get_data(user_id)) is None:
        raise not_found_error
    if user_data.user_company_role != OrganizerRole.company:
        raise forbiden_error
    return user_data