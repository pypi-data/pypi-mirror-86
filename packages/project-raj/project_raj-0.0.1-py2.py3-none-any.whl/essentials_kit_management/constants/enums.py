import enum

class StatusEnum(enum.Enum):
    LIVE = "LIVE"
    CLOSED = "CLOSED"
    DONE = "DONE"


class TransactionTypeEnum(enum.Enum):
    GOOGLE_PAY = "GOOGLE_PAY"
    PHONE_PAY = "PHONE_PAY"
    PAYTM = "PAYTM"


class VerificationChoicesEnum(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
