# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management_v2"
OPERATION_NAME = "get_wallet_transaction_details"
REQUEST_METHOD = "get"
URL_SUFFIX = "wallet_transactions/v1/"

from .test_case_01 import TestCase01GetWalletTransactionDetailsAPITestCase

__all__ = [
    "TestCase01GetWalletTransactionDetailsAPITestCase"
]
