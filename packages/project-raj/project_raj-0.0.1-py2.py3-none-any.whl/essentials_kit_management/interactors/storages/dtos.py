from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from essentials_kit_management.constants.enums \
    import StatusEnum, VerificationChoicesEnum


@dataclass
class AccessTokenDto:
    access_token: str
    refresh_token: str
    expires_in: int


@dataclass
class FormDto:
    form_id: int
    form_name: str
    form_description: str
    form_status: StatusEnum
    close_date: datetime
    expected_delivery_date: datetime


@dataclass
class OrderedItemDto:
    ordered_item_id: int
    user_id: int
    item_id: int
    brand_id: int
    form_id: int
    item_price: float
    ordered_quantity: int
    delivered_quantity: int
    is_out_of_stock: int


@dataclass
class FormsListMetricsDto:
    form_id: int
    items_count: int
    estimated_cost: float
    items_pending: int
    cost_incurred: float


@dataclass
class CompleteFormsDetailsDto:
    total_forms_count: int
    form_dtos: List[FormDto]
    ordered_item_dtos: List[OrderedItemDto]


@dataclass
class ItemDto:
    item_id: int
    section_id: int
    item_name: str
    item_description: str


@dataclass
class BrandDto:
    item_id: int
    brand_id: int
    brand_name: str
    item_price: float
    min_quantity: int
    max_quantity: int


@dataclass
class SectionDto:
    section_id: int
    form_id: int
    product_title: str
    product_description: str


@dataclass
class FormDetailsDto:
    form_id: int
    form_name: str
    form_description: str
    close_date: datetime
    section_dtos: List[SectionDto]
    item_dtos: List[ItemDto]
    brand_dtos: List[BrandDto]


@dataclass
class CompleteFormDetailsDto:
    form_details_dto: FormDetailsDto
    ordered_item_dtos: List[OrderedItemDto]


@dataclass
class FormMetricsDto:
    total_cost: float
    total_items: int


@dataclass
class UserOrderDetailsDto:
    ordered_item_id: int
    item_id: int
    item_name: int
    item_price: float
    ordered_quantity: int
    delivered_quantity: int
    is_out_of_stock: int


@dataclass
class ItemMetricsDto:
    item_id: int
    item_name: str
    quantity_added_for_item: int
    cost_incurred_for_item: float
    quantity_received_for_item: int
    is_out_of_stock: bool


@dataclass
class OrderedFormMetricsDto:
    total_items_count: int
    total_cost_incurred: float
    total_received_items_count: int


@dataclass
class OrderDetailsOfFormDto:
    form_id: int
    item_metrics_dtos: List[ItemMetricsDto]
    form_metrics_dto: FormMetricsDto


@dataclass
class TransactionDetailsDto:
    transaction_id: int
    transaction_date: datetime
    credit_amount: float
    debit_amount: float
    verification_status: Optional[VerificationChoicesEnum]
    remarks: str


@dataclass
class WalletTransactionDetailsDto:
    wallet_balance: int
    transaction_details_dtos: List[TransactionDetailsDto]
