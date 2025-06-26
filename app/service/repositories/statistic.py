from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import(
    Contract as ContractModel,
    Supply as SupplyModel,
    Product as ProductModel,
    ExpenseCompany as ExpenseCompanyModel,
)

from service.items_services.dashboard.statistic_map_item import (
    SuppliesStatisticOfMonthItem,
    GeneralStatisticCompany,
    GeneralStatisticSupplier,
    FilterForGettingGraphStatistic
)



class StatisticRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_graph_supplies_statistics_by_organizer(
            self,
            organizer: FilterForGettingGraphStatistic
    ) -> Optional[List[dict]]:
        """Получить статистику поставок по компании за месяц"""
        select_query = select(
            func.date_trunc("month", SupplyModel.created_at).label("month"),
            func.count(SupplyModel.id).label("count")
        )

        if organizer.organizer_role == "supplier":
            stmt = (
                select_query
                .where(SupplyModel.supplier_id == organizer.organization_id)
                .group_by("month")
                .order_by("month")
            )
        elif organizer.organizer_role == "company":
            stmt = (
                select_query
                .where(SupplyModel.company_id == organizer.organization_id)
                .group_by("month")
                .order_by("month")
            )

        result = await self.session.execute(stmt)
        supplies_statistics = result.mappings().all()

        return [
            SuppliesStatisticOfMonthItem(**statistic).dict
            for statistic in supplies_statistics
        ] if supplies_statistics else None

    async def get_general_statistics_by_company_id(
            self,
            company_id: int
    ) -> Optional[GeneralStatisticCompany]:
        """Получить общую статистику по компании"""
        stmt = (
            select(
                select(func.count(SupplyModel.id))
                .where(SupplyModel.company_id == company_id).label("all_supplies_count"),
                # TODO: Оптимизировать
                select(func.count(SupplyModel.id))
                .where(
                    SupplyModel.company_id == company_id,
                    SupplyModel.is_wait_confirm
                ).label("is_wait_confirm_supplies_count"),
                select(func.count(ExpenseCompanyModel.id))
                .where(ExpenseCompanyModel.company_id == company_id).label("count_adopted_products"),
                select(func.count(ContractModel.id))
                .where(ContractModel.company_id == company_id).label("organizers_contract_count")
            )
        )

        result = await self.session.execute(stmt)
        mapping_obj = result.mappings().first()
        return GeneralStatisticCompany.from_dict(parse_dict=mapping_obj) if mapping_obj else None

    async def get_general_statistics_by_supplier_id(
            self,
            supplier_id: int
    ) -> Optional[GeneralStatisticSupplier]:
        """Получить общую статистику по поставщику"""
        stmt = (
            select(
                select(func.count(SupplyModel.id))
                .where(SupplyModel.supplier_id == supplier_id).label("all_supplies_count"),
                # TODO: Оптимизировать
                select(func.count(SupplyModel.id))
                .where(
                    SupplyModel.supplier_id == supplier_id,
                    SupplyModel.is_wait_confirm
                ).label("is_wait_confirm_supplies_count"),
                select(func.count(ProductModel.id))
                .where(ProductModel.supplier_id == supplier_id).label("all_products_count"),
                select(func.count(ContractModel.id))
                .where(ContractModel.supplier_id == supplier_id).label("organizers_contract_count")
            )
        )

        result = await self.session.execute(stmt)
        mapping_obj = result.mappings().first()
        return GeneralStatisticSupplier.from_dict(parse_dict=mapping_obj) if mapping_obj else None
