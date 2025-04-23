from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import *
from service.items_services.items import *

from utils import generate_unique_code


class LinkCodeService:
    """Класс бизнес-логики работы с пригласительным кодом"""
    def __init__(self, session: AsyncSession):
        self.link_code_repo = LinkCodeRepository(
            session=session, 
        )

    async def create_link_code(self, user_id: int) -> None:
        """Метод для создания пригласительного кода"""
        code = generate_unique_code()
        link_code = LinkCodeItem(
            code=code,
            user_id=user_id
        )
        await self.link_code_repo.create(link_code)
