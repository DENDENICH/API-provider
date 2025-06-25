from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


from models import(
    UserCompany as UserCompanyModel,
    User as UserModel,

)
from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.items import(
    UserCompanyItem,
    UserCompanyWithUserItem
)


class UserCompanyRepository(BaseRepository[UserCompanyModel]):
    """Репозиторий бизнес логики работы с уч. записью пользователя в организации"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(UserCompanyModel, session=session, item=UserCompanyItem)

    async def get_by_user_id(self, user_id: int) -> Optional[UserCompanyItem]:
        result = await self.session.execute(
            select(self.model).filter(self.model.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_all_employ_by_organizer_id(
            self,
            organizer_id: int
    ) -> Optional[List[UserCompanyWithUserItem]]:
        """Получить всех сотрудников по ID организатора"""
        stmt = (
            select(
                self.model.user_id,
                self.model.role,
                UserModel.name,
                UserModel.email,
                UserModel.phone
            )
            .join(UserModel, UserModel.id == self.model.user_id)
            .where(self.model.organizer_id == organizer_id)
            .filter()
        )
        result = await self.session.execute(stmt)
        models = result.mappings().all()
        if models is None:
            return None
        users = [UserCompanyWithUserItem(**dict(user)) for user in models]
        return users

    async def delete_by_user_and_organizer_id(
            self,
            user_id: int,
            organizer_id: int
    ) -> bool:
        query = delete(UserCompanyModel).where(
            UserCompanyModel.user_id == user_id,
            UserCompanyModel.organizer_id == organizer_id
        )
        result = await self.session.execute(query)
        # Возвращаем False, если результат изменения = 0
        return False if result.rowcount == 0 else True