from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Expense as ExpenseModel
from app.service.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[ExpenseModel]):
    """Адаптер для работы с БД"""
    def __init__(self, session: AsyncSession):
        super().__init__(ExpenseModel, session=session)
