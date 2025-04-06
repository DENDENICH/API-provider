from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.repositories import *
from app.service.items_services.items import *
from app.service.items_services.to_items_functions import *


class UserService:
    """Класс бизнес-логики работы с пользователем"""
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session, to_item=user_to_item)
        self.link_code_repo = LinkCodeRepository(session, to_item=link_code_to_item)
        self.user_company_repo = UserCompanyRepository(session, to_item=user_company_to_item)

    async def get_user_by_id(self, user_id: int) -> Optional[UserItem]:
        """Получить пользователя по ID"""
        if (user := await self.user_repo.get_by_id(user_id)) is None:
            pass
            # TODO: exception
        return user

    async def get_user_company_by_user_id(self, user_id: int) -> Optional[UserCompanyItem]:
        """Получить данные участника компании по его user_id"""
        return await self.user_company_repo.get_by_id(user_id)
        #TODO: доделать

    async def get_user_response(self, user_id: int) -> Dict[
        Literal["user"]: UserItem, Literal["user_company"]: UserCompanyItem
    ]:
        """Получить представление пользователя (User + UserCompany)"""
        if (user_response := self.user_repo.get_user_with_company(user_id=user_id)) is None:
            pass
            # TODO: исключение, если такой пользователь не найден
        return {
            "user": user_response[0],
            "user_company": user_response[1]
        }

    async def assign_user_to_company(self, user_id: int, role: str) -> UserCompanyItem:
        """Назначить пользователя в компанию с ролью"""
        user_company = UserCompanyItem(organizer_id=0, user_id=user_id, role=role)  # organizer_id позже будет указан
        return await self.user_company_repo.create(user_company)

    async def remove_user_from_company(self, user_id: int) -> None:
        """Удалить пользователя из компании"""
        user_company = await self.user_company_repo.get_by_user_id(user_id)
        if user_company:
            await self.user_company_repo.delete(user_company.id) 

