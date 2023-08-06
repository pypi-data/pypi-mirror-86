# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management"
OPERATION_NAME = "get_form_details"
REQUEST_METHOD = "get"
URL_SUFFIX = "forms/{form_id}/v1/"

from .test_case_01 import TestCase01GetFormDetailsAPITestCase
from .test_case_02 import TestCase02GetFormDetailsAPITestCase

__all__ = [
    "TestCase01GetFormDetailsAPITestCase",
    "TestCase02GetFormDetailsAPITestCase"
]
