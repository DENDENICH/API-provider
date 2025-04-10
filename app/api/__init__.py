from fastapi import APIRouter

from .user_api import router as router_user
from .supply_api import router as router_supplies
from .product_api import router as router_products
from .organizer_api import router as router_organizer
from .supplier_api import router as router_supplier
from .expense_api import router as router_expense

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
router.include_router(
    router=router_organizer
)
router.include_router(
    router=router_supplier
)
router.include_router(
    router=router_expense
)
