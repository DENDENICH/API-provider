from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.user_service import User
from app.models import Users as UserModel
from app.service.repositories.base_repository import BaseRepository, ServiceObj


class UserRepository(BaseRepository[UserModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session=session)

    async def get_user_by_email(self, email: str) -> ServiceObj:
        """Получить пользователя по email"""
        result = await self.session.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
 