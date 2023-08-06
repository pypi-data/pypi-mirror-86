# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management_v2"
OPERATION_NAME = "get_forms_as_list"
REQUEST_METHOD = "get"
URL_SUFFIX = "forms/v1/"

from .test_case_01 import TestCase01GetFormsAsListAPITestCase

__all__ = [
    "TestCase01GetFormsAsListAPITestCase"
]
