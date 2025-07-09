from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from fastapi import (
    APIRouter, 
    Depends,
    Query, 
    status
)

from core import settings

from api.dependencies import check_is_supplier, get_user_from_redis

from api.dependencies import (
    check_is_supplier, 
    get_user_from_redis,
    get_session
)

from schemas.product import (
    ProductRequestCreate,
    ProductRequestUpdate,
    ProductResponse,
    ProductsResponse
)
from schemas.expense import ExpenseResponse

from service.bussines_services.product import ProductService
from service.items_services.product import ProductVersionItem, ProductCreate
from service.redis_service import UserDataRedis


router = APIRouter(
    tags=settings.api.products.tags,
    prefix=settings.api.products.prefix,
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductRequestCreate,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(get_session)
):
    """Create product"""
    service = ProductService(session=session)
    expense = await service.create_product(
        user_data=user_data,
        product_new=ProductCreate(**product_in.model_dump())
    )

    await session.commit()
    return ExpenseResponse(**expense.dict)


@router.get("", response_model=ProductsResponse)
async def get_products(
    supplier_id: Optional[int] = Query(None),
    add_quantity: Optional[bool] = Query(False),
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(get_session),
):
    """Get products"""
    service = ProductService(session=session)
    products = await service.get_available_products_for_company(
        company_id=user_data.organizer_id,
        supplier_id=supplier_id,
        add_quantity=add_quantity
    )
    return ProductsResponse(products=[ProductResponse(id=product.id, **product.dict) for product in products])
    

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int,
    user_data: UserDataRedis = Depends(get_user_from_redis),
    session: AsyncSession = Depends(get_session)
):
    """Get product by id"""
    service = ProductService(session)
    product = await service.get_product_by_id(product_id)
    return ProductResponse(id=product.id, **product.dict)



@router.put("/{product_id}", response_model=ExpenseResponse)
async def update_product(
    product_id: int,
    product_in: ProductRequestUpdate,
    user_data: UserDataRedis = Depends(check_is_supplier),
    session: AsyncSession = Depends(get_session)
):
    """Update product by id"""
    service = ProductService(session)
    product = await service.update_product(
        product_id, 
        ProductVersionItem(**product_in.model_dump())
    )
    await session.commit()
    return ExpenseResponse(**product.dict)
