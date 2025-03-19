from typing import Optional, Type

from .base_service import BaseService, Model


class OrganizerService(BaseService):
    def __init__(self,
                 role: str,
                 name: str,
                 address: str,
                 inn: str,
                 bank_details: str,
                 id_: Optional[int] = None, 
                 model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.role = role
        self.address = address
        self.name = name
        self.inn = inn
        self.bank_details = bank_details



