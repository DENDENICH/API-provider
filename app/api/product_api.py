from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from fastapi import APIRouter, Depends, Request, status, HTTPException, Query

from core import settings
from core.db import db_core

from api.dependencies import check_is_company, check_is_supplier

from schemas.product import (
    ProductRequest,
    ProductResponse,
    ProductsResponse
)

from service.bussines_services.product import ProductService
from service.items_services.product import ProductFullItem, ProductVersion
from service.redis_service import UserDataRedis

from logger import logger


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
    try:
        service = ProductService(session=session)
        product = await service.create_product(
            user_data=user_data,
            **product_in.model_dump()
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating user company\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    await session.commit()
    return ProductResponse(id=product.id, **product.dict)


@router.get("/", response_model=ProductsResponse)
async def get_products(
    supplier_id: Optional[int] = Query(None),
    add_quantity: Optional[bool] = Query(False),
    user_data: UserDataRedis = Depends(check_is_company),
    session: AsyncSession = Depends(db_core.session_getter),
):
    service = ProductService(session=session)
    products = await service.get_available_products_for_company(
        company_id=user_data.organizer_id,
        supplier_id=supplier_id,
        add_quantity=add_quantity
    )
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
    product_in: ProductRequest,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(db_core.session_getter)
):
    try:
        service = ProductService(session)
        product: ProductFullItem = await service.update_product(
            product_id, 
            ProductVersion(**product_in.model_dump())
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            msg="Error creating user company\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    await session.commit()
    return ProductResponse(id=product.id, **product.dict)

    