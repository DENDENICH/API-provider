from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status

from core import settings
from core.db import db_core

from schemas.product import (
    ProductRequest,
    ProductResponse,
    ProductsResponse
)

from service.busines_service import ProductService
from service.items_services.items import ProductItem

router = APIRouter(
    tags=settings.api.products.tags,
    prefix=settings.api.products.prefix,
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: Request,
    product_in: ProductRequest,
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session=session)
    product = await service.create_product(**product_in.model_dump())
    return ProductResponse(id=product.id, **product.dict)


@router.get("/", response_model=ProductsResponse)
async def get_all_products(
    request: Request,
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session=session)
    # TODO: redis хранение
    supplier_id = None
    products = await service.get_all_products(supplier_id)
    return ProductsResponse(products=products)
    


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session)
    product = await service.get_product_by_id(product_id)
    return ProductResponse(**product.dict)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    request: Request,
    product_id: int,
    product_in: ProductResponse,
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session)
    product = await service.update_product(
        product_id, 
        ProductItem(product_in.model_dump()
        )
    )
    return ProductResponse(**product.dict)
    