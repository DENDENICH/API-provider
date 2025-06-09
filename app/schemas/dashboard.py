from pydantic import BaseModel
from typing import List
from enum import Enum


class SuppliesStatisticOfMonthItem(BaseModel):
    month: str
    count: int

class StatisticBase(BaseModel):
    all_supplies_count: int
    is_wait_confirm_supplies_count: int
    organizers_contract_count: int
    supplies_statistic_of_month: List[SuppliesStatisticOfMonthItem] | List

class StatisticCompany(StatisticBase):
    count_adopted_products: int

class StatisticSupplier(StatisticBase):
    all_products_count: int
    