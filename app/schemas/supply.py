from typing import List
from enum import Enum
from pydantic import BaseModel

from schemas.organizer import OrganizerSupplyObject
from schemas.product import ProductResponseSupply


class CancelledAssembleStatus(str, Enum):
    cancelled = "cancelled"
    assemble = "assemble"

class StatusForUpdate(str, Enum):
    assemble = "assemble"
    in_delivery = "in_delivery"
    adopted = "adopted"
    delivery = "delivery"


class SupplyBase(BaseModel):
    supplier_id: int
    delivery_address: str
    total_price: float


class SupplyProduct(BaseModel):
    """Сущность продукта в поставке"""
    product: ProductResponseSupply
    quantity: int


class SupplyProductCreate(BaseModel):
    product_id: int
    quantity: int


class SupplyCreateRequest(SupplyBase):
    supply_products: List[SupplyProductCreate]


class SupplyResponse(BaseModel):
    delivery_address: str
    total_price: float
    supplier: OrganizerSupplyObject
    supply_products: List[SupplyProduct]
    article: int
    status: str
    create_datetime: str
    is_wait_confirm: bool
    # couriers_phone: str
    # delivery_datetime: Optional[str]


class SuppliesResponse(BaseModel):
    supplies: List[SupplyResponse]


class SuppliesCancelledAssembleStatus(BaseModel):
    status: CancelledAssembleStatus


class SupplyStatusUpdate(BaseModel):
    status: StatusForUpdate