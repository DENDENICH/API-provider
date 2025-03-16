from fastapi import APIRouter

from core import settings


router = APIRouter(
    tags=settings.api.products.tags,
    prefix=settings.api.products.prefix,
)

