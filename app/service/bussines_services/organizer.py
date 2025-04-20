from typing import Optional, Dict, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import *
from service.items_services.items import *
from service.redis_service import redis

from exceptions import bad_request_error


class OrganizerService:
    """Класс бизнес-логики для работы с организацией"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.organizer_repo = OrganizerRepository(session=session)
        self.user_company_repo = UserCompanyRepository(session=session)
    
    async def register_company_with_admin(
        self,
        name: str,
        address: str,
        inn: str,
        bank_details: str,
        role: str,
        id: int
    ) -> OrganizerItem:
        """Регистрация компании и создание администратора организации"""
        existing = await self.user_company_repo.get_by_user_id(user_id=id)
        if existing:
            raise bad_request_error(detail="User existing in company")
        organizer = OrganizerItem(
            name=name,
            role=role,
            address=address,
            inn=inn,
            bank_details=bank_details
        )
        organizer = await self.organizer_repo.create(organizer)

        return organizer