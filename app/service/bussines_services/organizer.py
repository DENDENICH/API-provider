from sqlalchemy.ext.asyncio import AsyncSession

from service.repositories import OrganizerRepository, UserCompanyRepository
from service.items_services.organizer import OrganizerItem

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
    
    async def get_supplier_by_inn(self, supplier_inn: int) -> OrganizerItem:
        """Получить поставщика по его ИНН"""
        supplier: OrganizerItem = await self.organizer_repo.get_supplier_by_inn(supplier_inn=supplier_inn)
        if not supplier:
            raise bad_request_error(detail="Supplier not found")
        return supplier
    