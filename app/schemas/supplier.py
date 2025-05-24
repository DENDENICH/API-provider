from typing import List
from pydantic import BaseModel

from schemas.organizer import OrganizerResponse


class SuppliersResponse(BaseModel):
    organizers: List[OrganizerResponse]


# Схема создания контракта между компанией и организатором
# SupplierProductResponse - списко продуктов