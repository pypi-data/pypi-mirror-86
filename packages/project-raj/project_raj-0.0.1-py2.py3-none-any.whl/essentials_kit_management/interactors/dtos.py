from dataclasses import dataclass
from essentials_kit_management.constants.enums import TransactionTypeEnum

@dataclass
class PostItemDetailsDto:
    item_id: int
    brand_id: int
    ordered_quantity: int


@dataclass
class PostVerificationDetailsDto:
    amount: float
    payment_transaction_id: int
    transaction_type: TransactionTypeEnum
    screenshot_url: str
