from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


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


class ProductResponse(ProductBase):
    id: int
    article: int
    description: str


class ProductResponseSupply(ProductBase):
    """Неполная информация о товаре для отображения на странице поставщика"""
    id: int
    article: int

class ProductsResponse(BaseModel):
    products: List[ProductResponseSupply]

