from fastapi import APIRouter

from .user_api import router as router_user
from .supplie_api import router as router_supplies
from .product_api import router as router_products

router = APIRouter()

router.include_router(
    router=router_user
)
router.include_router(
    router=router_supplies
)
router.include_router(
    router=router_products
)
