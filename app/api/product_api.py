from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from app.core import settings
from app.core.db import db_core

from app.schemas.product import (
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
    pass

@router.get("/products", response_model=ProductsResponse)
async def get_products(
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    product_data: ProductResponse, 
    session: AsyncSession = Depends(db_core.session_getter)
):
    pass

