from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


# TODO: Добавить фильтры получения всех сущностей во всех схемах

class UserRole(str, Enum):
    company = "admin"
    supplier = "manager"
    employee = "employee"

class UserTypeForNextRoute(str, Enum):
    """Тип перенаправления пользователя после регистрации"""
    employee = "employee"
    organizer = "organizer"


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserSchema(UserBase):
    """Модель пользователя"""
    id: int
    phone: str

class UserCompanySchema(BaseModel):
    """Модель уч. записи пользователя в компании"""
    link_code: int
    role: UserRole

class UserCompanyWithUserSchema(BaseModel):
    """Модель уч. записи пользователя в компании с данными пользователя"""
    user_id: int
    role: UserRole
    name: str
    email: EmailStr
    phone: str

class UsersCompanyWithUserSchema(BaseModel):
    """Модель уч. записи пользователя в компании с данными пользователя"""
    users: list[UserCompanyWithUserSchema]

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


class AuthTokenSchema(BaseModel):
    """Аутентификационый токен"""
    access_token: str
    type_token: str

class AuthTokenSchemaAfterRegister(AuthTokenSchema):
    next_route: str

class AuthTokenSchemaAfterLogin(AuthTokenSchema):
    role_organizer: str
    user_role: UserRole