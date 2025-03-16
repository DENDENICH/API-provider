from fastapi import APIRouter

from .users import router as router_user
from .supplies import router as router_supplies
from .products import router as router_products

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
