from models import *
from service.items_services.items import *


def organizer_to_item(model: Organizer) -> OrganizerItem:
    return OrganizerItem(**model.dict(), model_=model)


def contract_to_item(model: Contract) -> ContractItem:
    return ContractItem(**model.dict(), model_=model)


def user_to_item(model: User) -> UserItem:
    return UserItem(**model.dict(), model_=model)


def user_company_to_item(model: UserCompany) -> UserCompanyItem:
    return UserCompanyItem(**model.dict(), model_=model)


def link_code_to_item(model: LinkCode) -> LinkCodeItem:
    return LinkCodeItem(**model.dict(), model_=model)


def product_to_item(model: Product) -> ProductItem:
    return ProductItem(**model.dict(), model_=model)


def product_version_to_item(model: ProductVersion) -> ProductVersionItem:
    return ProductVersionItem(**model.dict(), model_=model)


def supply_to_item(model: Supply) -> SupplyItem:
    return SupplyItem(**model.dict(), model_=model)


def supply_product_to_item(model: SupplyProduct) -> SupplyProductItem:
    return SupplyProductItem(**model.dict(), model_=model)


def expense_company_to_item(model: ExpenseCompany) -> ExpenseCompanyItem:
    return ExpenseCompanyItem(**model.dict(), model_=model)


def expense_supplier_to_item(model: ExpenseSupplier) -> ExpenseSupplierItem:
    return ExpenseSupplierItem(**model.dict(), model_=model)


__all__ = [
    "organizer_to_item",
    "contract_to_item",
    "user_to_item",
    "user_company_to_item",
    "link_code_to_item",
    "product_to_item",
    "product_version_to_item",
    "supply_to_item",
    "supply_product_to_item",
    "expense_company_to_item",
    "expense_supplier_to_item"
]