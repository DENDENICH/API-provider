from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import(
    Organizer as OrganizerModel,
    User as UserModel,
    UserCompany as UserCompanyModel,
    LinkCode as LinkCodeModel,

)
from service.repositories.base_repository import(
     BaseRepository,
)
from service.items_services.items import(
    UserItem,
    UserCompanyItem,
)

from service.redis_service import UserDataRedis


class UserRepository(BaseRepository[UserModel]):
    """Репозиторий бизнес логики работы с уч. записью пользователя"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(UserModel, session=session, item=UserItem)

    async def get_by_email(self, email: str) -> Optional[UserItem]:
        """Получить пользователя по email"""
        result = await self.session.execute(
            select(self.model).filter(self.model.email == email)
        )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_user_with_company(self, user_id: int) -> Tuple[Optional[UserItem], Optional[UserCompanyItem]]:
        """Получить пользователя и его связь с компанией по user_id"""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.user_company))
            .filter(self.model.id == user_id)
        )
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None, None

        user_item = self.item(**user_model.dict, model=user_model)
        user_company_model: UserCompanyModel = user_model.user_company[0] if user_model.user_company else None
        user_company_item = self.item(
            **user_company_model.dict,
            model=user_company_model
        ) if user_company_model else None

        return user_item, user_company_item

    async def get_user_by_link_code(self, link_code: int) -> Optional[UserItem]:
        """Получение пользователя по link code"""
        stmt = (
            select(LinkCodeModel)
            .options(joinedload(LinkCodeModel.user))
            .where(LinkCodeModel.code == link_code)
        )
        result = await self.session.execute(stmt)
        link_code_model = result.scalar_one_or_none()

        if link_code_model is None:
            return None

        user_model: UserModel = link_code_model.user
        user_item = self.item(**user_model.dict, model=user_model) if link_code_model.user else None
        return user_item

    async def get_user_context_by_user_id(self, user_id: int) -> Optional[UserDataRedis]:
        """Получить контекст пользователя по user_id"""
        stmt = (
            select(
                UserCompanyModel.id.label("user_company_id"),
                UserCompanyModel.role.label("user_company_role"),
                OrganizerModel.id.label("organizer_id"),
                OrganizerModel.role.label("organizer_role")
            )
            .join(OrganizerModel, OrganizerModel.id == UserCompanyModel.organizer_id)
            .where(UserCompanyModel.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        row = result.mappings().first()
        return UserDataRedis(**dict(row)) if row else None
