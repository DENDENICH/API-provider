from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SupplyProduct as SupplyProductModel
from app.service.repositories.base_repository import BaseRepository, ServiceObj


class UserRepository(BaseRepository[SupplyProductModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(SupplyProductModel, session=session)
