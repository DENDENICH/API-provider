from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from organizer import OrganizerSupplyObject
from product import ProductResponseSupply

class SupplyBase(BaseModel):
    supplier_id: int
    delivery_address: str
    total_price: float


class SupplyProduct(BaseModel):
    product: ProductResponseSupply
    quantity: int


class SupplyCreateRequest(SupplyBase):
    supply_products: List[SupplyProduct]


class SupplyResponse(SupplyBase):
    supplier: OrganizerSupplyObject
    supply_products: List[ProductResponseSupply]
    couriers_phone: str
    article: int
    status: str


class SupplyStatusUpdate(BaseModel):
    status: str