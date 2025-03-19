from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Supply as SupplyModel
from app.service.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[SupplyModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(SupplyModel, session=session)
