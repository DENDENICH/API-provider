from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, Enum):
    company = "company"
    supplier = "supplier"


class UserBase(BaseModel):
    """Базовая модель валидации пользователя"""
    name: str
    email: str


class UserRegisterRequest(UserBase):
    role: UserRole
    phone: str


class UserSchema(UserBase):
    id: int
    role: UserRole
    phone: str


class UserLoginRequest(BaseModel):
    email: str
    password: str