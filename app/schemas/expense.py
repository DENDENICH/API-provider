from typing import List, Optional
from pydantic import BaseModel

from schemas.product import ProductCategory


class ExpenseResponse(BaseModel):
    """Объект расхода"""
    id: Optional[int] = None
    article: int
    supplier_name: Optional[str] = None
    product_id: int
    product_name: str
    category: ProductCategory
    quantity: int
    description: Optional[str] = None


class ExpensesResponse(BaseModel):
    """Объект списка расходов"""
    expenses: List[ExpenseResponse]


class ExpenseQuantity(BaseModel):
    """Объект количества расхода"""
    quantity: int

