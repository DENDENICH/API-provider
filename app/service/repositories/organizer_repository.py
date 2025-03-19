from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organizer
from app.service.repositories.base_repository import BaseRepository


class OrganizerRepository(BaseRepository[Organizer]):
    """Репозиторий для работы с моделями Organizer"""
    def __init__(self, session: AsyncSession):
        super().__init__(Organizer, session=session)
