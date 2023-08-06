# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management"
OPERATION_NAME = "get_pay_through_details"
REQUEST_METHOD = "get"
URL_SUFFIX = "pay_through/details/v1/"

from .test_case_01 import TestCase01GetPayThroughDetailsAPITestCase

__all__ = [
    "TestCase01GetPayThroughDetailsAPITestCase"
]
