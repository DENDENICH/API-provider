from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Organizer as OrganizerModel,
    Product as ProductModel,
    ProductVersion as ProductVersionModel,
    ExpenseSupplier as ExpenseSupplierModel,
)
from service.repositories.base_repository import(
     BaseRepository,
)

from service.items_services.expense import (
    ExpenseWithInfoProductItem,
    ExpenseSupplierItem,
)


class ExpenseSupplierRepository(BaseRepository[ExpenseSupplierModel]):
    """Репозиторий бизнес логики работы с складом поставщика"""

    def __init__(
            self,
            session: AsyncSession,
    ):
        super().__init__(ExpenseSupplierModel, session=session, item=ExpenseSupplierItem)

    async def get_all_expense_response_items(
            self,
            supplier_id: int
    ) -> Optional[List[ExpenseWithInfoProductItem]]:
        """Получить все расходы по supplier_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_id,
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, self.model.supplier_id == OrganizerModel.id)
            .join(ProductModel, self.model.product_id == ProductModel.id)
            .join(ProductVersionModel, ProductModel.product_version_id == ProductVersionModel.id)
            .where(self.model.supplier_id == supplier_id)
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
            supplier_id: int,
            product_id: int
    ) -> Optional[ExpenseWithInfoProductItem]:
        """Получить расход по supplier_id и product_id"""
        stmt = (
            select(
                self.model.id,
                self.model.product_id,
                self.model.quantity,
                ProductModel.article,
                ProductVersionModel.name.label("product_name"),
                ProductVersionModel.category,
                ProductVersionModel.description,
                OrganizerModel.name.label("supplier_name")
            )
            .join(OrganizerModel, self.model.supplier_id == OrganizerModel.id)
            .join(ProductModel, self.model.product_id == ProductModel.id)
            .join(ProductVersionModel, ProductModel.product_version_id == ProductVersionModel.id)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.product_id == product_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.mappings().first()
        return ExpenseWithInfoProductItem(**dict(expense)) if expense is not None else None

    async def get_by_expense_and_supplier_id(
            self,
            supplier_id: int,
            expense_id: int,
    ) -> Optional[ExpenseSupplierItem]:
        """Получить товар по id поставщика и id расхода"""
        stmt = (
            select(self.model)
            .where(
                self.model.supplier_id == supplier_id,
                self.model.id == expense_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseSupplierItem(**expense.dict) if expense is not None else None

    async def get_by_product_and_supplier_id(
            self,
            product_id: int,
            supplier_id: int,
    ) -> Optional[ExpenseSupplierItem]:
        """Получить по id продукта и поставщика"""
        stmt = (
            select(self.model)
            .where(
                self.model.product_id == product_id,
                self.model.supplier_id == supplier_id
            )
        )
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseSupplierItem(**expense.dict) if expense is not None else None
