from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status

from core import settings
from core.db import db_core

from api.dependencies import check_is_company, check_is_supplier

from schemas.product import (
    ProductRequest,
    ProductResponse,
    ProductsResponse
)

from service.bussines_services.product import ProductService
from service.items_services.items import ProductItem
from service.redis_service import UserDataRedis

router = APIRouter(
    tags=settings.api.products.tags,
    prefix=settings.api.products.prefix,
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductRequest,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session=session)
    product = await service.create_product(**product_in.model_dump())
    return ProductResponse(id=product.id, **product.dict)


@router.get("/", response_model=ProductsResponse)
async def get_products(
    user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(db_core.session_getter),
):
    service = ProductService(session=session)
    #TODO: 
    products = await service.get_available_products_for_company(user_data.organizer_id)
    return ProductsResponse(products=products)
    

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int,
    user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session)
    product = await service.get_product_by_id(product_id)
    return ProductResponse(**product.dict)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_in: ProductResponse,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    service = ProductService(session)
    product = await service.update_product(
        product_id, 
        **ProductItem(product_in.model_dump())
    )
    return ProductResponse(**product.dict)
    