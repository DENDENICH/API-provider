from typing import Tuple, Optional, List, Iterable

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

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
)
from service.items_services.items import *
from service.items_services.product import (
    ProductVersion,
    ProductItem,
    ProductFullItem,
    AvailableProductForCompany
)
from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseSupplierItem,
    ExpenseCompanyItem
)
from service.items_services.organizer import OrganizerItem
from service.items_services.contract import ContractItem
from service.items_services.supply import (
    SupplyProductItem,
    SupplyResponseItem,
    SupplyItem
)
from service.redis_service import UserDataRedis


class OrganizerRepository(BaseRepository[OrganizerModel]):
    """Репозиторий бизнес логики работы с организатором"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(OrganizerModel, session=session, item=OrganizerItem)
    
    async def get_supplier_by_inn(self, inn: str) -> Optional[OrganizerItem]:
        """Получить поставщика по его ИНН"""
        result = await self.session.execute(
            select(self.model).filter(
                self.model.inn == inn,
                self.model.role == "supplier"
            )
        )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


class ContactRepository(BaseRepository[ContractModel]):
    """Репозиторий бизнес логики работы с контрактами"""
    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ContractModel, session=session, item=ContractItem)

    async def get_by_company_and_supplier_id(self, company_id: int, supplier_id: int) -> Optional[ContractItem]:
        """Получение контракта по id компании и поставщика"""
        stmt = select(self.model).filter(
                self.model.company_id == company_id,
                self.model.supplier_id == supplier_id
            )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_supplier_available_company(self, company_id: int) -> List[OrganizerItem]:
        """Получить поставщиков с которыми заключены контракты"""
        stmt = (
            select(OrganizerModel)
            .join(self.model, self.model.supplier_id == OrganizerModel.id)
            .where(self.model.company_id == company_id)
        )
        result = await self.session.execute(stmt)
        suppliers = result.scalars().all()
        return [self.item(**supplier.dict, model=supplier) for supplier in suppliers]

    async def delete(self, supplier_id: int, company_id: int) -> bool:
        """Удалить контракт по id поставщика"""
        stmt = (
            delete(self.model)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.company_id == company_id
            )
        )
        result = await self.session.execute(stmt)
        # Возвращаем False, если результат изменения = 0
        return False if result.rowcount == 0 else True



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
            

class LinkCodeRepository(BaseRepository[LinkCodeModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self, 
            session: AsyncSession
    ):
        super().__init__(LinkCodeModel, session=session, item=LinkCodeItem)

    async def get_code_by_user_id(self, user_id: int) -> Optional[LinkCodeItem]:
        result = await self.session.execute(
            select(self.model).filter(self.model.user_id == user_id)
            )
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None


class ProductRepository(BaseRepository[ProductModel]):
    """Репозиторий бизнес логики работы с товаром"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(ProductModel, session=session, item=ProductItem)

    async def get_by_id_full_product(self, id: int) -> ProductFullItem:
        """Получить объект по ID"""
        result = await self.session.execute(
            select(
                self.model.id,
                self.model.article,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.description,
                ProductVersionModel.img_path
            )
            .join(
                ProductVersionModel, 
                self.model.product_version_id == ProductVersionModel.id
            )
            .where(self.model.id == id)
        )
        product = result.mappings().first()
        return self.item(**dict(product)) if product is not None else None

    async def get_all_products(
            self, 
            supplier_id: int, 
            limit: int = 20
    ) -> Optional[List[ProductFullItem]]:
        """Получение всех продуктов"""
        stmt = (
            select(
                self.model.id,
                self.model.article,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.img_path
            )
            .join(ProductVersionModel, self.model.product_version_id == ProductVersionModel.id)
            .where(self.model.supplier_id == supplier_id)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        products = result.mappings().all()

        if products is None:
            return None
        
        products = [ProductFullItem(**dict(p)) for p in products]

        return products
    
    async def get_available_products_for_company(
            self, 
            company_id: int,
            supplier_id: Optional[int] = None,
            limit: int = 100        
    ) -> Optional[List[AvailableProductForCompany]]:
        """Получить все доступные товары для компании по её ID"""
        stmt = (
            select(
                self.model.id,
                self.model.article,
                self.model.supplier_id,
                ProductVersionModel.name,
                ProductVersionModel.category,
                ProductVersionModel.price,
                ProductVersionModel.img_path,
                OrganizerModel.name.label("organizer_name")
            )
            .join(ProductVersionModel, self.model.product_version_id == ProductVersionModel.id)
            .join(OrganizerModel, OrganizerModel.id == self.model.supplier_id)
            .join(ContractModel, ContractModel.supplier_id == self.model.supplier_id)
            .where(
                ContractModel.company_id == company_id,
                ContractModel.supplier_id == supplier_id,
            )
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        products = result.mappings().all()

        if products is None:
            return None
        
        products = [AvailableProductForCompany(**dict(p)) for p in products]

        return products
    
    async def get_products_by_supplies_products(
            self, 
            supply_products: Iterable[SupplyProductItem]
    ) -> Iterable[ProductItem]:
        """Получить все продукты по id продуктов в поставке"""
        products_version_ids = [supply_product.product_version_id for supply_product in supply_products]
        stmt = (
            select(ProductVersionModel.product)
            .where(ProductVersionModel.id.in_(products_version_ids))
        )
        result = await self.session.execute(stmt)
        products: Iterable[ProductModel] = result.scalars().all()
        return [self.item(**p.dict()) for p in products]
    

class ProductVersionRepository(BaseRepository[ProductVersionModel]):
    """Репозиторий бизнес логики работы с версией товара"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(ProductVersionModel, session=session, item=ProductVersion)

    async def get_products_version_by_products_ids(
            self,
            products_ids: Iterable[int]
    ) -> Iterable[ProductItem]:
        """Получить id всех версий продуктов по id продуктов"""
        stmt = (
            select(ProductModel.product_version)
            .where(ProductModel.id.in_(products_ids))
        )
        result = await self.session.execute(stmt)
        products_version: Iterable[ProductVersionModel] = result.scalars().all()
        return [self.item(**p.dict()) for p in products_version]

class SupplyRepository(BaseRepository[SupplyModel]):
    """Репозиторий бизнес логики работы с поставкой"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(LinkCodeModel, session=session, item=SupplyItem)

    async def update(self, obj: SupplyItem, supplier_id: int) -> Optional[SupplyItem]:
        """Обновить объект поставки"""
        query = update(self.model).where(
            self.model.id == obj.id, self.model.supplier_id == supplier_id
        ).values(**obj.dict).returning(self.model)
        
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self.item(**model.dict, model=model) if model is not None else None

    async def get_all_by_organizer_id(
            self, 
            supplier_id: Optional[int] = None,
            company_id: Optional[int] = None,
            is_wait_confirm: Optional[bool] = None        
    ) -> Optional[List[SupplyResponseItem]]:
        """Получить все поставки по id поставщика"""
        supplier = aliased(OrganizerModel)
        company = aliased(OrganizerModel)

        stmt = (
            select(
                self.model.id,
                self.model.article,
                self.model.delivery_address,
                self.model.total_price,
                self.model.status,
                self.model.created_at,

                supplier.id.label("supplier_id"),
                supplier.name.label("supplier_name"),

                company.id.label("company_id"),
                company.name.label("company_name"),

                SupplyProductModel.quantity,
                
                ProductModel.id.label("product_id"),
                ProductModel.article.label("product_article"),
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category.label("product_category"),
                ProductVersionModel.price.label("product_price")
            )
            .join(supplier, SupplyModel.supplier_id == supplier_id or supplier.id)
            .join(company, SupplyModel.company_id == company_id or company.id)
            .join(SupplyProductModel, SupplyModel.id == SupplyProductModel.supply_id)
            .join(ProductModel, ProductVersionModel.product)
            .join(ProductVersionModel, ProductModel.product_version_id == ProductVersionModel.id)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.is_wait_confirm == is_wait_confirm
            )
        )
        result = await self.session.execute(stmt)
        if (supplies := result.mappings().all()) is None:
            return None
        return [SupplyResponseItem.get_from_dict(dict(supply)) for supply in supplies]
    
    async def get_supply_products_by_supply_id(self, supply_id: int) -> List[SupplyProductItem]:
        """Получить все продукты в поставке по id поставки"""
        stmt = (
            select(
                SupplyProductModel.id,
                SupplyProductModel.supply_id,
                SupplyProductModel.product_version_id,
                SupplyProductModel.quantity,
                ProductModel.article.label("product_article"),
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category.label("product_category"),
                ProductVersionModel.price.label("product_price")
            )
            .join(ProductModel, ProductVersionModel.product)
            .join(ProductVersionModel, ProductVersionModel.id == ProductModel.product_version_id)
            .where(SupplyProductModel.supply_id == supply_id)
        )
        result = await self.session.execute(stmt)
        if (products := result.mappings().all()) is None:
            return None
        return [SupplyProductItem(**dict(product)) for product in products]    
    

class SupplyProductRepository(BaseRepository[SupplyProductModel]):
    """Репозиторий бизнес логики работы c продуктом в поставке"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(LinkCodeModel, session=session, item=SupplyProductItem)

    async def create_all(
            self, 
            products: Iterable[SupplyProductItem]
    ) -> None:
        """Создать объекты"""
        models = [self.model(**product.dict) for product in products]
        self.session.add_all(models)

    async def get_by_supply_id(
            self,
            supply_id: int
    ) -> Iterable[SupplyProductItem]:
        """Получить продукты из поставок по id поставки"""
        stmt = (
            select(self.model)
            .where(self.model.supply_id == supply_id)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.item(**model.dict()) for model in models] if models is not None else None


class ExpenseCompanyRepository(BaseRepository[ExpenseCompanyModel]):
    """Репозиторий бизнес логики работы с складом компании"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(LinkCodeModel, session=session, item=ExpenseCompanyModel)

    async def get_all_expense_response_items(
            self, 
            company_id: int
    ) -> Optional[List[ExpenseWithInfoProductItem]]:
        """Получить все расходы по company_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_version_id.label("product_id"),
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, OrganizerModel.id == ProductModel.supplier_id)
            .join(ProductModel, ProductModel.product_version_id == ProductVersionModel.id)
            .join(ProductVersionModel, self.model.product_version)    
            .where(self.model.company_id == company_id)
        )
        result = await self.session.execute(stmt)
        expenses = result.mappings().all()
        if expenses is None:
            return None
        expenses_items = [
            ExpenseWithInfoProductItem(**dict(expense)) for expense in expenses
            ]
        return expenses_items
    
    async def get_expense_response_items(
            self, 
            company_id: int,
            product_version_id: int
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получить расход по company_id и product_version_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_version_id.label("product_id"),
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, OrganizerModel.id == ProductModel.supplier_id)
            .join(ProductModel, ProductModel.product_version_id == ProductVersionModel.id)
            .join(ProductVersionModel, self.model.product_version)    
            .where(
                self.model.company_id == company_id,
                self.model.product_version_id == product_version_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.mappings().first()
        return ExpenseWithInfoProductItem(**dict(expense)) if expense is not None else None
    
    async def get_by_expense_and_company_id(
            self,
            expense_id: int,
            company_id: int
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получение сущности расхода по id компании и расхода"""
        stmt = (
            select(
                self.model.id,
                self.model.product_version_id.label("product_id"),
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, OrganizerModel.id == ProductModel.supplier_id)
            .join(ProductModel, ProductModel.product_version_id == ProductVersionModel.id)
            .join(ProductVersionModel, self.model.product_version)
            .where(
                self.model.company_id == company_id,
                self.model.id == expense_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseWithInfoProductItem(**expense.dict) if expense is not None else None


class ExpenseSupplierRepository(BaseRepository[ExpenseSupplierModel]):
    """Репозиторий бизнес логики работы с складом поставщика"""
    def __init__(
            self, 
            session: AsyncSession,
    ):
        super().__init__(LinkCodeModel, session=session, item=ExpenseSupplierModel)

    async def get_all_expense_response_items(
            self, 
            supplier_id: int
    ) -> Optional[List[ExpenseWithInfoProductItem]]:
        """Получить все расходы по supplier_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_id,
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, self.model.supplier)
            .join(ProductVersionModel, ProductVersionModel.id == ProductModel.product_version_id)
            .join(ProductModel, self.model.product)    
            .where(self.model.supplier_id == supplier_id)
        )
        result = await self.session.execute(stmt)
        expenses = result.mappings().all()
        if expenses is None:
            return None
        expenses_items = [
            ExpenseWithInfoProductItem(**dict(expense)) for expense in expenses
            ]
        return expenses_items
    
    async def get_expense_response_items(
            self, 
            supplier_id: int,
            product_id: int
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получить расход по supplier_id и product_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_id,
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, self.model.supplier)
            .join(ProductVersionModel, ProductVersionModel.id == ProductModel.product_version_id)
            .join(ProductModel, self.model.product)    
            .where(
                self.model.supplier_id == supplier_id,
                self.model.product_id == product_id    
            )
        
        )
        result = await self.session.execute(stmt)
        expense = result.mappings().first()
        return ExpenseWithInfoProductItem(**dict(expense)) if expense is not None else None
    
    async def get_by_expense_and_supplier_id(
            self, 
            supplier_id: int,
            expense_id: int,
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получить товар по id поставщика и id расхода"""
        stmt = (
            select(
                self.model.id,
                self.model.product_id,
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, self.model.supplier)
            .join(ProductVersionModel, ProductVersionModel.id == ProductModel.product_version_id)
            .join(ProductModel, self.model.product)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.id == expense_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseWithInfoProductItem(**expense.dict) if expense is not None else None
    
    async def get_by_product_and_supplier_id(
            self, 
            product_id: int,
            supplier_id: int,
    ) -> Optional[ExpenseSupplierItem]:
        """Получить по id продукта и поставщика"""
        stmt = (
            select(self.model)
            .where(
                self.model.product_id == product_id,
                self.model.supplier_id == supplier_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseSupplierItem(**expense.dict) if expense is not None else None
    