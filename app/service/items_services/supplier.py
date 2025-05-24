from typing import Optional
from dataclasses import dataclass, field

@dataclass
class FilterGetSupplier:
    is_company_contracts: bool
    inn: Optional[int] = field(default=None)
