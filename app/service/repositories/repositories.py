from typing import Callable, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import( 
    Organizer as OrganizerModel,
    Contract as ContractModel,
    User as UserModel,
    UserCompany as UserCompanyModel,
    LinkCode as LinkCodeModel,
    SupplyProduct as SupplyProductModel,
    Supply as SupplyModel,
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
    ExpenseCompany as ExpenseCompanyModel,
    ExpenseSupplier as ExpenseSupplierModel,
)
from service.repositories.base_repository import(
     BaseRepository,
     ItemObj
)
from service.items_services.items import *


class OrganizerRepository(BaseRepository[OrganizerModel]):
    """Репозиторий бизнес логики работы с организатором"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[OrganizerModel], ItemObj]):
        super().__init__(OrganizerModel, session=session, to_item=to_item)


class ContactRepository(BaseRepository[ContractModel]):
    """Репозиторий бизнес логики работы с контрактами"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[ContractModel], ItemObj]):
        super().__init__(ContractModel, session=session, to_item=to_item)


class UserRepository(BaseRepository[UserModel]):
    """Репозиторий бизнес логики работы с уч. записью пользователя"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[UserModel], UserItem]):
        super().__init__(UserModel, session=session, to_item=to_item)

    async def get_by_email(self, email: str) -> Optional[UserItem]:
        """Получить пользователя по email"""
        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self.to_item(model) if model is not None else None
    
    async def get_user_with_company(self, user_id: int) -> Tuple[
        Optional[UserItem], Optional[UserCompanyItem]
    ]:
        """Получить пользователя и его связь с уч. записи в компании по user_id"""
        stmt = (
            select(UserModel)
            .options(joinedload(UserCompanyModel.user_id))
            .filter(UserModel.id == user_id)
        )
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None, None

        user_item = self.to_item(user_model)
        user_company_model = user_model.user_company[0] if user_model.user_company else None
        user_company_item = self.to_item(user_company_model) if user_company_model else None

        return user_item, user_company_item


class UserCompanyRepository(BaseRepository[UserCompanyModel]):
    """Репозиторий бизнес логики работы с уч. записью пользователя в организации"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[UserCompanyModel], ItemObj]):
        super().__init__(UserCompanyModel, session=session, to_item=to_item)

    async def get_by_user_id(self, user_id: int) -> Optional[UserCompanyItem]:
        result = await self.session.execute(
            select(UserCompanyModel).filter(UserCompanyModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self.to_item(model) if model is not None else None


class LinkCodeRepository(BaseRepository[LinkCodeModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)

    async def get_code_by_user_id(self, user_id: int) -> ItemObj:
        result = await self.session.execute(
            select(LinkCodeModel).filter(LinkCodeModel.user_id == user_id)
            )
        model = result.scalar_one_or_none()
        return self.to_item(model) if model is not None else None


class ProductRepository(BaseRepository[ProductModel]):
    """Репозиторий бизнес логики работы с товаром"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)

    async def get_available_products_for_company(company_id: int):
        """Получить все доступные товары для компании по её ID"""
        pass


class ProductVersionRepository(BaseRepository[ProductVersionModel]):
    """Репозиторий бизнес логики работы с версией товара"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[ProductVersionModel], ItemObj]):
        super().__init__(ProductVersionModel, session=session, to_item=to_item)


class SupplyRepository(BaseRepository[SupplyModel]):
    """Репозиторий бизнес логики работы с поставкой"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)


class SupplyProductRepository(BaseRepository[SupplyProductModel]):
    """Репозиторий бизнес логики работы c продуктом в поставке"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)


class ExpenseCompanyRepository(BaseRepository[ExpenseCompanyModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)


class ExpenseSupplierRepository(BaseRepository[ExpenseSupplierModel]):
    """Репозиторий бизнес логики работы с складом поставщика"""
    def __init__(
            self, 
            session: AsyncSession,
            to_item: Callable[[LinkCodeModel], ItemObj]):
        super().__init__(LinkCodeModel, session=session, to_item=to_item)
