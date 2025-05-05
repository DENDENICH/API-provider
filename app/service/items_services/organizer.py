from typing import Optional, Type

from .base import Model, BaseItem


class OrganizerItem(BaseItem):
    """Объект организации"""
    def __init__(self,
                 role: str,
                 name: str,
                 address: str,
                 inn: str,
                 bank_details: str,
                 id: Optional[int] = None, 
                 model: Optional[Type[Model]] = None
    ):
        super().__init__(id=id, model=model)
        
        self.role = role
        self.address = address
        self.name = name
        self.inn = inn
        self.bank_details = bank_details