from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Organizer as OrganizerModel

from service.repositories.base_repository import BaseRepository

from service.items_services.organizer import OrganizerItem


class OrganizerRepository(BaseRepository[OrganizerModel]):
    """Репозиторий бизнес логики работы с организатором"""

    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(OrganizerModel, session=session, item=OrganizerItem)

    async def get_supplier_by_inn(self, inn: str) -> Optional[OrganizerItem]:
        """Получить поставщика по его ИНН"""
        # Обработка нескольких найденых вариантов
        stmt = (
            select(self.model)
            .filter(self.model.role == "supplier")
            .where(self.model.inn == inn)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model else None
