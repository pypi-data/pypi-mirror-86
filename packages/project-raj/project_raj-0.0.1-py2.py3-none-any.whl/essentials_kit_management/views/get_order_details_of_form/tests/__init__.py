# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management"
OPERATION_NAME = "get_order_details_of_form"
REQUEST_METHOD = "get"
URL_SUFFIX = "forms/{form_id}/order_details/v1/"

from .test_case_01 import TestCase01GetOrderDetailsOfFormAPITestCase
from .test_case_02 import TestCase02GetOrderDetailsOfFormAPITestCase

__all__ = [
    "TestCase01GetOrderDetailsOfFormAPITestCase",
    "TestCase02GetOrderDetailsOfFormAPITestCase"
]
