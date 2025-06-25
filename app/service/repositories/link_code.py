from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import LinkCode as LinkCodeModel

from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.items import LinkCodeItem


class LinkCodeRepository(BaseRepository[LinkCodeModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self,
            session: AsyncSession
    ):
        super().__init__(LinkCodeModel, session=session, item=LinkCodeItem)

    async def get_code_by_user_id(self, user_id: int) -> Optional[LinkCodeItem]:
        result = await self.session.execute(
            select(self.model).filter(self.model.user_id == user_id)
            )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None
