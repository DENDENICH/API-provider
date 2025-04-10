from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr


# TODO: Добавить фильтры получения всех сущностей во всех схемах

class UserRole(str, Enum):
    company = "admin"
    supplier = "manager"
    employee = "employee"

class UserTypeForNextRoute(str, Enum):
    """Тип перенаправления пользователя после регистрации"""
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserSchema(UserBase):
    """Модель пользователя"""
    id: int
    phone: str

class UserCompanySchema(BaseModel):
    """Модель уч. записи пользователя в компании"""
    id: int
    role: UserRole
    organizer_id: int

class UserRegisterRequest(UserBase):
    """Модель запроса на регистрацию"""
    phone: str
    password: str
    # тип перенаправления
    user_type: UserTypeForNextRoute

class UserLoginRequest(BaseModel):
    """Модель запроса на вход"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Модель пользователя - ответ"""
    user: UserSchema
    user_company: Optional[UserCompanySchema]


class AuthTokenSchema(BaseModel):
    """Аутентификационый токен"""
    access_token: str
    type_token: str
    next_route: Optional[str]
