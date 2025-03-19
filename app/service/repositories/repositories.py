from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import( 
    Expense as ExpenseModel,
    Organizer as OrganizerModel,
    SupplyProduct as SupplyProductModel,
    Supply as SupplyModel,
    User as UserModel,
    Product as ProductModel
)
from app.service.repositories.base_repository import(
     BaseRepository,
     ServiceObj
)


class UserRepository(BaseRepository[UserModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session=session)

    async def get_user_by_email(self, email: str) -> ServiceObj:
        """Получить пользователя по email"""
        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        return result.scalar_one_or_none()


class SupplyRepository(BaseRepository[SupplyModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(SupplyModel, session=session)


class SupplyProductRepository(BaseRepository[SupplyProductModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(SupplyProductModel, session=session)


class ProductRepository(BaseRepository[ProductModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(ProductModel, session=session)


class OrganizerRepository(BaseRepository[OrganizerModel]):
    """Репозиторий для работы с моделями Organizer"""
    def __init__(self, session: AsyncSession):
        super().__init__(OrganizerModel, session=session)


class ExpenseRepository(BaseRepository[ExpenseModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(ExpenseModel, session=session)


