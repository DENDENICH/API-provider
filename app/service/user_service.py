from typing import Optional, Type

from .base_service import BaseService, Model


class UserService(BaseService):
    def __init__(self,
                 role: str,
                 name: str,
                 email: str,
                 phone: str,
                 password: str,
                 company_id: int,
                 id_: Optional[int] = None, 
                 model_: Optional[Type[Model]] = None
    ):
        super().__init__(id_=id_, model_=model_)
        
        self.role = role
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.company_id = company_id



