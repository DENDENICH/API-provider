from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import (
    UserRepository,
    UserCompanyRepository,
    LinkCodeRepository
)
from service.items_services.items import (
    UserCompanyItem,
    UserCompanyWithUserItem,
    UserItem
)
from service.redis_service import redis_user, UserDataRedis

from exceptions.exceptions import NotFoundError, BadRequestError


class UserService:
    """Класс бизнес-логики работы с пользователем"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session=session)
        self.link_code_repo = LinkCodeRepository(session=session)
        self.user_company_repo = UserCompanyRepository(session=session)        

    async def get_user_by_id(self, user_id: int) -> Optional[UserItem]:
        """Получить пользователя по ID"""
        if (user := await self.user_repo.get_by_id(user_id)) is None:
            raise NotFoundError("User not found")
        return user

    async def _get_user_by_link_code(self, link_code: int) -> Optional[UserItem]:
        """Получение пользователя по пригласительному коду LinkCodeModel"""
        if (user_item := await self.user_repo.get_user_by_link_code(link_code)) is None:
            raise NotFoundError("User not found")
        return user_item

    async def assign_user_to_company_by_link_code(
            self,
            user_data: UserDataRedis,
            link_code: int,
            role: str,
    ) -> UserCompanyItem:
        """Назначить пользователя в компанию с ролью"""

        user = await self._get_user_by_link_code(link_code)
        if user is None:
            raise NotFoundError("User not found")
        
        user_company = await self.user_company_repo.get_by_user_id(
            user_id=user.id
        )
        if user_company:
            raise BadRequestError("User already in company")

        user_company = UserCompanyItem(
            organizer_id=user_data.organizer_id, 
            user_id=user.id,
            role=role
        )
        return await self.user_company_repo.create(user_company)
    
    
    async def get_all_employ_by_organizer_id(
            self,
            organizer_id: int,
    ) -> List[UserCompanyWithUserItem]:
        """Получить всех сотрудников по ID организатора"""
        users = await self.user_company_repo.get_all_employ_by_organizer_id(
            organizer_id=organizer_id
        )
        if not users:
            raise NotFoundError("Users not found")
        return users
    
    async def assign_admin_to_company(
        self,
        user_id: int,
        organizer_id: int,
        role: str = "admin"
    ) -> UserCompanyItem:
        """Назначить администратора в организацию"""
        user_company = UserCompanyItem(
            organizer_id=organizer_id, 
            user_id=user_id, 
            role=role
        ) 

        admin = await self.user_company_repo.create(user_company)
        return admin

    async def update_user(self, user_id: int, user: UserItem) -> UserItem:
        """Обновление данных пользователя"""
        if (
            user_item := await self.user_repo.update(obj_id=user_id, obj=user)
        ) is None:
            raise NotFoundError("User not found")
        return user_item

    async def remove_user_from_company(
            self, 
            user_data: UserDataRedis, 
            user_for_remove_id: int
        ) -> None:
        """Удалить пользователя из компании"""
        result = await self.user_company_repo.delete_by_user_and_organizer_id(
            user_id=user_for_remove_id,
            organizer_id=user_data.organizer_id
        )
        if not result:
            raise NotFoundError("User not found")
    
    async def set_data_user_to_redis(
        self, 
        user_id: int,
        user_context: UserDataRedis = None
    ) -> UserDataRedis:
        """Сохранить данные пользователя в Redis"""
        if user_context is None:
            if (user_context := await self.user_repo.get_user_context_by_user_id(user_id)) is None:

                return UserDataRedis(
                    user_id=user_id,
                    organizer_role="not_have_organizer",
                    user_company_role="not_have_role",
                )
        await redis_user.set_data(
            key=user_id,
            data=user_context
        )
        return user_context
        