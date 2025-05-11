from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ProductCategory(str, Enum):
    hair_coloring = "hair_coloring"
    hair_care = "hair_care"
    hair_styling = "hair_styling"
    consumables = "consumables"
    perming = "perming"
    eyebrows = "eyebrows"
    manicure_and_pedicure = "manicure_and_pedicure"
    tools_and_equipment = "tools_and_equipment"


class ProductBase(BaseModel):
    name: str
    category: ProductCategory
    price: float


class ProductRequest(ProductBase):
    description: str
    quantity: int


class ProductResponse(ProductBase):
    id: int
    article: int
    supplier_id: int
    quantity: Optional[int]
    description: Optional[str]


class ProductResponseSupply(ProductBase):
    """Неполная информация о товаре для отображения на странице поставщика"""
    id: int
    article: int

class ProductsResponse(BaseModel):
    products: List[ProductResponse]

