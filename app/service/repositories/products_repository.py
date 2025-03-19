from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product as ProductModel
from app.service.repositories.base_repository import BaseRepository, ServiceObj


class ProductRepository(BaseRepository[ProductModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(ProductModel, session=session)


