from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from service.repositories import StatisticRepository
from service.items_services.dashboard.dashboard import StatisticResponseItem
from service.items_services.dashboard.statistic_map_item import (
    GeneralStatisticCompany,
    GeneralStatisticSupplier,
    SuppliesStatisticOfMonthItem,
    FilterForGettingGraphStatistic
)

from service.redis_service import UserDataRedis

from exceptions import NotFoundError


class StaticticService:
    """Класс бизнес-логики работы с пригласительным кодом"""
    def __init__(self, session: AsyncSession):
        self.statistic_repo = StatisticRepository(
            session=session, 
        )

    async def get_statistics_by_company(self, organizer: UserDataRedis) -> dict:
        """Получение всей статистики компании"""
        graph_statistics = await self._get_graph_supplies_statistics(organizer)

        if (general_statistic := await self.statistic_repo.get_general_statistics_by_company_id(
                company_id=organizer.organizer_id
            )
        ) is None:
            raise NotFoundError("Статистика компании не найдена")
        
        return StatisticResponseItem.get_response_schema_statistic(
            general_statistic=general_statistic,
            supplies_statistic_of_month=graph_statistics,
        )
    
    async def get_statistics_by_supplier(self, organizer: UserDataRedis) -> dict:
        """Получение всей статистики поставщика"""
        graph_statistics = await self._get_graph_supplies_statistics(organizer)

        if (general_statistic := await self.statistic_repo.get_general_statistics_by_supplier_id(
                supplier_id=organizer.organizer_id
            )
        ) is None:
            raise NotFoundError("Статистика поставщика не найдена")
        
        return StatisticResponseItem.get_response_schema_statistic(
            general_statistic=general_statistic,
            supplies_statistic_of_month=graph_statistics,
        )
    
    async def _get_graph_supplies_statistics(
            self, 
            organizer: UserDataRedis
    ) -> List[dict]:
        """Получение статистики поставок по месяцам"""
        if (result := await self.statistic_repo.get_graph_supplies_statistics_by_organizer(
            FilterForGettingGraphStatistic(
                organization_id=organizer.organizer_id,
                organizer_role=organizer.organizer_role
            )
        )) is None:
            raise NotFoundError("Статистика поставок не найдена")
        return result



