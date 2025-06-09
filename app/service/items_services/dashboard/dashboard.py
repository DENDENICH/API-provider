from typing import Optional, Type, TypeVar, Any
from functools import singledispatchmethod

from dataclasses import dataclass
from datetime import datetime

from enum import Enum

from service.items_services.dashboard.statistic_map_item import (
    GeneralStatisticBase,
    SuppliesStatisticOfMonthItem
)

T = TypeVar("T", bound=GeneralStatisticBase)

class StatisticResponseItem:
    """Конструктор для статистики"""
    
    @staticmethod
    def get_response_schema_statistic(
        general_statistic: Type[T],
        supplies_statistic_of_month: list[dict] | list,
    ) -> dict[str, Any]:
        """Формирование ответа со статистикой для API"""
        response: dict[str, Any] = general_statistic.dict
        response["supplies_statistic_of_month"] = supplies_statistic_of_month
        return response

        

