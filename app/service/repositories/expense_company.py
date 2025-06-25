from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Organizer as OrganizerModel,
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
    ExpenseCompany as ExpenseCompanyModel,

)
from service.repositories.base_repository import BaseRepository

from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseCompanyItem
)


class ExpenseCompanyRepository(BaseRepository[ExpenseCompanyModel]):
    """Репозиторий бизнес логики работы с складом компании"""

    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ExpenseCompanyModel, session=session, item=ExpenseCompanyItem)

    async def get_all_expense_response_items(
            self,
            company_id: int
    ) -> Optional[List[ExpenseWithInfoProductItem]]:
        """Получить все расходы по company_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_version_id.label("product_id"),
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                OrganizerModel.name.label("supplier_name")
            )
            .join(ProductVersionModel, self.model.product_version_id == ProductVersionModel.id)
            .join(ProductModel, ProductVersionModel.id == ProductModel.product_version_id)
            .join(OrganizerModel, ProductModel.supplier_id == OrganizerModel.id)
            .where(self.model.company_id == company_id)
        )
        result = await self.session.execute(stmt)
        expenses = result.mappings().all()
        if expenses is None:
            return None
        expenses_items = [
            ExpenseWithInfoProductItem(**dict(expense)) for expense in expenses
        ]
        return expenses_items

    async def get_expense_response_items(
            self,
            company_id: int,
            product_version_id: int
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получить расход по company_id и product_version_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_version_id.label("product_id"),
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(ProductVersionModel, self.model.product_version_id == ProductVersionModel.id)
            .join(ProductModel, ProductVersionModel.id == ProductModel.product_version_id)
            .join(OrganizerModel, ProductModel.supplier_id == OrganizerModel.id)
            .where(
                self.model.company_id == company_id,
                self.model.product_version_id == product_version_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.mappings().first()
        return ExpenseWithInfoProductItem(**dict(expense)) if expense is not None else None

    async def get_by_expense_and_company_id(
            self,
            expense_id: int,
            company_id: int
    ) -> Optional[ExpenseCompanyItem]:
        """Получение сущности расхода по id компании и расхода"""
        stmt = (
            select(self.model)
            .where(
                self.model.company_id == company_id,
                self.model.id == expense_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseCompanyItem(**expense.dict) if expense is not None else None
