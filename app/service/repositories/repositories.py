from typing import Callable, Tuple, Optional, Dict, TypedDict

from sqlalchemy import select, delete
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
from service.redis_service import UserContext


class OrganizerRepository(BaseRepository[OrganizerModel]):
    """Репозиторий бизнес логики работы с организатором"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(OrganizerModel, session=session, item=OrganizerItem)


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
    ):
        super().__init__(UserModel, session=session, item=UserItem)

    async def get_by_email(self, email: str) -> Optional[UserItem]:
        """Получить пользователя по email"""
        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None
    
    async def get_user_with_company(self, user_id: int) -> Tuple[Optional[UserItem], Optional[UserCompanyItem]]:
        """Получить пользователя и его связь с компанией по user_id"""
        stmt = (
            select(UserModel)
            .options(joinedload(UserModel.user_company))
            .filter(UserModel.id == user_id)
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
        
        #TODO:
        user_model: UserModel = link_code_model.user
        user_item = self.item(**user_model.dict, model=user_model) if link_code_model.user else None
        return user_item
    
    async def get_user_context_by_user_id(self, user_id: int) -> Optional[UserContext]:
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
        return UserContext(**dict(row)) if row else None


class UserCompanyRepository(BaseRepository[UserCompanyModel]):
    """Репозиторий бизнес логики работы с уч. записью пользователя в организации"""
    def __init__(
            self, 
            session: AsyncSession,
        ):
        super().__init__(UserCompanyModel, session=session, item=UserCompanyItem)

    async def get_by_user_id(self, user_id: int) -> Optional[UserCompanyItem]:
        result = await self.session.execute(
            select(UserCompanyModel).filter(UserCompanyModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None
    
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
            

class LinkCodeRepository(BaseRepository[LinkCodeModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self, 
            session: AsyncSession
    ):
        super().__init__(LinkCodeModel, session=session, item=LinkCodeItem)

    async def get_code_by_user_id(self, user_id: int) -> Optional[LinkCodeItem]:
        result = await self.session.execute(
            select(LinkCodeModel).filter(LinkCodeModel.user_id == user_id)
            )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


class ProductRepository(BaseRepository[ProductModel]):
    """Репозиторий бизнес логики работы с товаром"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(LinkCodeModel, session=session, item=ProductItem)

    async def get_available_products_for_company(company_id: int):
        """Получить все доступные товары для компании по её ID"""
        pass

    async def get_all_products(self, supplier_id: int, limit: int = 20):
        """Получение всех продуктов"""
        stmt = (
            select(
                ProductModel.id,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.description,
                ProductVersionModel.price
            )
            .join(ProductVersionModel, ProductModel.product_version_id == ProductVersionModel.id)
            .where(ProductModel.supplier_id == supplier_id)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        product_model_list = result.scalars()

        if product_model_list is None:
            return None
        
        products = [self.item(**model.dict) for model in product_model_list]

        return products


class ProductVersionRepository(BaseRepository[ProductVersionModel]):
    """Репозиторий бизнес логики работы с версией товара"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(ProductVersionModel, session=session, item=ProductItem)


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
