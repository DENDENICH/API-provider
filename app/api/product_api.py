from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from core import settings
from core.db import db_core

from schemas.product import (
    ProductRequest,
    ProductResponse,
    ProductResponseSupply,
    ProductsResponse
)


router = APIRouter(
    tags=settings.api.products.tags,
    prefix=settings.api.products.prefix,
)


@router.post("/products", status_code=201)
async def add_product(
    product_data: ProductRequest, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Добавление нового товара"""
    pass

@router.get("/products", response_model=ProductsResponse)
async def get_all_products(
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получение списка товаров"""
    pass

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получение информации о товаре"""
    pass

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    product_data: ProductResponse, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Обновление товара"""
    pass


@router.get("/products/{supplier_id}")
async def get_all_products_from_supplier(
    supplier_id: int,
    session: AsyncSession = Depends(db_core.session_getter)
):
    """Получение всех продуктов конкретного поставщика"""
    pass