from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import UserRepository
from service.items_services.items import UserItem


from auth.utils.hashing_password import hashing_password
from auth.utils.jwt_processes import jwt_processes as jwt

from exceptions import NotFoundError, BadRequestError


class UserAuthService:
    """Класс бизнес-логики работы с пользователем"""
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session=session)

    async def check_login_user(self, email: str, password: str) -> UserItem:
        """Получить пользователя по email"""
        if (user := await self.user_repo.get_by_email(email)) is None:
            raise NotFoundError("User not found")
        if not hashing_password.check_password(password=password, hash=user.password):
            raise NotFoundError("User not found")
        return user
    
    async def register_user(self, name: str, email: str, phone: str, password: str) -> UserItem:
        """Зарегистрировать нового пользователя"""
        # проверка на существование пользователя в БД
        if await self.user_repo.get_by_email(email=email):
            raise BadRequestError("User already exists")
        hashed_password = hashing_password.create_hash(password)
        user = UserItem(
            name=name, 
            email=email, 
            phone=phone, 
            password=hashed_password
        )
        return await self.user_repo.create(user)
    
    def get_jwt(self, user: UserItem, type_token: str = "Bearer") -> Dict[
        Literal["access_token"] | Literal["type_token"], str  
    ]:
        """Формирование и получение jwt токена для аутентификации"""
        token = jwt.encode_jwt(payload={'sub': str(user.id)})
        return {
            "access_token": token,
            "type_token": type_token
        }

