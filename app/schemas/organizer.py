from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


# 🔹 Запрос на регистрацию организации
class OrganizerRegisterRequest(BaseModel):
    name: str
    role: OrganizerRole
    address: str
    inn: str
    bank_details: str
    # Данные для регистрации администратора
    name_admin: str
    password: str
    email: EmailStr
    phone: str


# 🔹 Список организаций
class OrganizerResponse(BaseModel):
    id: int
    name: str
    role: OrganizerRole
    address: str
    inn: str
    bank_details: str


class OrganizersResponse(BaseModel):
    organizers: List[OrganizerResponse]


class OrganizerSupplyObject(BaseModel):
    id: int
    name: str