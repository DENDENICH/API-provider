from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import *
from service.items_services.items import *

from exceptions import forbiden_error, not_found_error, bad_request_error

from utils import generate_unique_code


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
            raise not_found_error
        return user

    async def get_user_company_by_user_id(self, user_id: int) -> Optional[UserCompanyItem]:
        """Получить данные участника компании по его user_id"""
        return await self.user_company_repo.get_by_id(user_id)
        #TODO: доделать

    async def get_user_by_link_code(self, id: int, link_code: int) -> Optional[UserItem]:
        """Получение пользователя по пригласительному коду LinkCodeModel"""
        if (user := await self.user_company_repo.get_by_user_id(user_id=id)) is None:
            raise bad_request_error("user is not in company")
        if user.role != "admin": 
            raise forbiden_error 
        
        if (user_item := await self.user_repo.get_user_by_link_code(link_code)) is None:
            raise not_found_error
        return user_item

    async def assign_user_to_company(
            self,
            id: int,
            user_id: int, 
            role: str,
    ) -> UserCompanyItem:
        """Назначить пользователя в компанию с ролью"""

        if (user := await self.user_company_repo.get_by_user_id(user_id=id)) is None:
            raise bad_request_error("user is not in company")
        if user.role != "admin": # регистрация только лицом администратора
            raise forbiden_error 

        user_company = UserCompanyItem(
            organizer_id=user.organizer_id, 
            user_id=user_id, 
            role=role
        ) 
        return await self.user_company_repo.create(user_company)
    
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
        if (user_item := await self.user_repo.update(
            obj_id=user_id, 
            obj=user
            )
        ) is None:
            raise not_found_error
        return user_item

    async def remove_user_from_company(self, id: int, user_id: int) -> None:
        """Удалить пользователя из компании"""
        if (user := await self.user_company_repo.get_by_user_id(user_id=id)) is None:
            raise bad_request_error("user is not in company")
        if user.role != "admin": 
            raise forbiden_error 
        
        result = await self.user_company_repo.delete_by_user_and_organizer_id(
            user_id=user_id,
            organizer_id=user.organizer_id
        )
        if not result:
            raise not_found_error


class OrganizerService:
    """Класс бизнес-логики для работы с организацией"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.organizer_repo = OrganizerRepository(session=session)
        self.user_company_repo = UserCompanyRepository(session=session)
    
    async def register_company_with_admin(
        self,
        name: str,
        address: str,
        inn: str,
        bank_details: str,
        role: str,
        id: int
    ) -> OrganizerItem:
        """Регистрация компании и создание администратора организации"""
        existing = await self.user_company_repo.get_by_user_id(user_id=id)
        if existing:
            raise bad_request_error(detail="User existing in company")
        organizer = OrganizerItem(
            name=name,
            role=role,
            address=address,
            inn=inn,
            bank_details=bank_details
        )
        organizer = await self.organizer_repo.create(organizer)

        return organizer
    

class LinkCodeService:
    """Класс бизнес-логики работы с пригласительным кодом"""
    def __init__(self, session: AsyncSession):
        self.link_code_repo = LinkCodeRepository(
            session=session, 
        )

    async def create_link_code(self, user_id: int) -> None:
        """Метод для создания пригласительного кода"""
        code = generate_unique_code()
        link_code = LinkCodeItem(
            code=code,
            user_id=user_id
        )
        await self.link_code_repo.create(link_code)


class ProductService:
    """Класс бизнес-логики работы с товарами"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session=session)
        self.version_repo = ProductVersionRepository(session=session)

    async def create_product(
            self,
            id: int, 
            name: str,
            category: str,
            price: float,
            description: str,
    ) -> ProductItem:
        """_summary_

        Args:
            id (int): Идентификатор пользователя
            name (str): Название продукта
            category (str): Категория продукта
            price (float): Цена продукта
            description (str): Описание продукта
            img_file (str): Ссылка на файл

        Returns:
            ProductItem: _description_
        """

        article = await generate_unique_code()

        # TODO: сделать реализацию сохранения картинки 
        img_file = None

        # Создаем версию продукта
        product_version_item = ProductItem(
            name=name,
            category=category,
            description=description,
            price=price,
            img_path=img_file
        )
        product_version: ProductItem = await self.version_repo.create(product_version_item)
        await self.session.flush()

        # Создаем продукт
        temp_product = ProductItem(
            article=article,
            product_version_id=product_version.id,
            supplier_id=id,
        )
        product: ProductItem = await self.product_repo.create(temp_product)
        await self.session.flush()

        return product
    
    async def get_all_products(self, supplier_id: int) -> list[ProductItem]:
        """Получить все продукты поставщика"""
        if (products := await self.product_repo.get_all_products(supplier_id=supplier_id)) is None:
            raise not_found_error
        return products
    
    async def get_product_by_id(self, product_id: int) -> Optional[ProductItem]:
        """Получить продукт по id"""
        if (product := await self.product_repo.get_by_id(id=product_id)) is None:
            raise not_found_error
        return product
    
    async def update_product(
            self, 
            product_id: int,
            product: ProductItem
        ) -> ProductItem: 
        """Обновить продукт"""
        if (user_item := await self.product_repo.update(
            obj_id=product_id,
            obj=product
            )
        ) is None:
            raise not_found_error
        return user_item

