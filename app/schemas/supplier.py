from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr

from organizer import OrganizerResponse
from supply import SupplyResponse


class SuppliesResponse(BaseModel):
    supplies: List[SupplyResponse]


class SuppliersResponse(BaseModel):
    organizers: List[OrganizerResponse]
