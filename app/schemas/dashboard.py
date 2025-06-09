    # SuppliesStatisticOfMonthItem:
    #   type: object
    #   properties:
    #     month:
    #       type: string
    #     count:
    #       type: integer
        
    # StatisticCompany:
    #   type: object
    #   allOf: '#/components/schemas/StatisticBase'
    #   properties:
    #     count_adopted_products:
    #       type: integer
    #     all_supplies_count:
    #       type: integer
    #     is_wait_confirm_supplies_count:
    #       type: integer
    #     organizers_contract_count:
    #       type: integer
    #     supplies_statistic_of_month:
    #       type: array
    #       items: 
    #         $ref: '#/components/schemas/SuppliesStatisticOfMonthItem'
        
    
    # StatisticSupplier:
    #   type: object
    #   allOf: '#/components/schemas/StatisticBase'
    #   properties:
#         all_products_count:
    #       type: integer
    #     all_supplies_count:
    #       type: integer
    #     is_wait_confirm_supplies_count:
    #       type: integer
    #     organizers_contract_count:
    #       type: integer
    #     supplies_statistic_of_month:
    #       type: array
    #       items: 
    #         $ref: '#/components/schemas/SuppliesStatisticOfMonthItem' 

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
    