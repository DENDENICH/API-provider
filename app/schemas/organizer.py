from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr


class OrganizerRole(str, Enum):
    company = "company"
    supplier = "supplier"


class OrganizerRegisterRequest(BaseModel):
    name: str
    role: OrganizerRole
    address: str
    inn: str
    bank_details: str


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