from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import *
from service.items_services.items import *
from service.items_services.to_items_functions import *

from exceptions import forbiden_error, not_found_error, bad_request_error


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
        """Получить представление пользователя"""
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


class OrganizerService:
    """Класс бизнес-логики для работы с организацией"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.organizer_repo = OrganizerRepository(session, to_item=organizer_to_item)
        self.user_company_repo = UserCompanyRepository(session, to_item=user_company_to_item)
    
    async def register_company_with_admin(
        self,
        name: str,
        address: str,
        inn: str,
        bank_details: str,
        user_id: int
    ) -> OrganizerItem:
        """Регистрация компании и создание администратора организации"""
        existing = await self.user_company_repo.get_by_user_id(user_id=user_id)
        if existing:
            raise bad_request_error(detail="User existing in company")
        organizer = OrganizerItem(
            name=name,
            role="company",
            address=address,
            inn=inn,
            bank_details=bank_details
        )
        organizer = await self.organizer_repo.create(organizer)

        admin_user = UserCompanyItem(
            user_id=user_id,
            organizer_id=organizer.id,
            role="admin"
        )
        await self.user_company_repo.create(admin_user)

        return organizer
    
