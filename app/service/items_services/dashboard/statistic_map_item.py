from sqlalchemy import RowMapping

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from utils.validate_datetime_str import ValidateYearMonthDate 


class GeneralStatisticBase(ABC):
    """Базовый класс статистики"""
    def __init__(
            self, 
            all_supplies_count: int,
            is_wait_confirm_supplies_count: int,
            organizers_contract_count: int,
        ):
        self.all_supplies_count = all_supplies_count
        self.is_wait_confirm_supplies_count = is_wait_confirm_supplies_count
        self.organizers_contract_count = organizers_contract_count

    @classmethod
    @abstractmethod
    def from_dict(cls, parse_dict: dict[str, Any] | RowMapping):
        pass
    
    @property
    @abstractmethod
    def dict(self) -> dict[str, Any]:
        """Возвращает словарь с атрибутами класса"""
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        if value is None:
            raise ValueError(f"Value for {name} cannot be None")
        object.__setattr__(self, name, value)


class GeneralStatisticCompany(GeneralStatisticBase):
    """Класс общей статистики компании"""

    def __init__(
            self, 
            all_supplies_count: int,
            is_wait_confirm_supplies_count: int,
            organizers_contract_count: int,
            count_adopted_products: int, 
        ):
        super().__init__(
            all_supplies_count,
            is_wait_confirm_supplies_count,
            organizers_contract_count
        )
        self.count_adopted_products = count_adopted_products

    @classmethod
    def from_dict(cls, parse_dict: dict[str, Any] | RowMapping):
        return cls(**parse_dict)

    @property
    def dict(self) -> dict[str, Any]:
        """Возвращает словарь с атрибутами класса"""
        return self.__dict__


class GeneralStatisticSupplier(GeneralStatisticBase):
    """Класс общей статистики поставщика"""

    def __init__(self, all_products_count: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_products_count = all_products_count

    @classmethod
    def from_dict(cls, parse_dict: dict[str, Any] | RowMapping):
        return cls(**parse_dict)

    @property
    def dict(self) -> dict[str, Any]:
        """Возвращает словарь с атрибутами класса"""
        return self.__dict__


class SuppliesStatisticOfMonthItem:
    def __init__(self, count: int, month: Any):
        self.month = month 
        self.count = count

    @property
    def month(self) -> str:
        return self._month
    
    @month.setter
    def month(self, value):
        self._month = ValidateYearMonthDate.validate(value)

    @property
    def dict(self) -> Dict:
        return {
            "month": self.month,
            "count": self.count
        }


@dataclass
class FilterForGettingGraphStatistic:
    organization_id: int
    organizer_role: str
    