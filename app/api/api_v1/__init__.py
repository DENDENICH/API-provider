from fastapi import APIRouter

from .users import router as users_router
from core import settings


router = APIRouter(
    prefix=settings.api.v1.prefix
)

# регистрация роутера пользователей в основной роутер v1 версии
router.include_router(router=users_router)