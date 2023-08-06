# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management"
OPERATION_NAME = "post_form_details"
REQUEST_METHOD = "post"
URL_SUFFIX = "forms/{form_id}/v1/"

from .test_case_01 import TestCase01PostFormDetailsAPITestCase
from .test_case_02 import TestCase02PostFormDetailsAPITestCase
from .test_case_03 import TestCase03PostFormDetailsAPITestCase
from .test_case_04 import TestCase04PostFormDetailsAPITestCase
from .test_case_05 import TestCase05PostFormDetailsAPITestCase
from .test_case_06 import TestCase06PostFormDetailsAPITestCase

__all__ = [
    "TestCase01PostFormDetailsAPITestCase",
    "TestCase02PostFormDetailsAPITestCase",
    "TestCase03PostFormDetailsAPITestCase",
    "TestCase04PostFormDetailsAPITestCase",
    "TestCase05PostFormDetailsAPITestCase",
    "TestCase06PostFormDetailsAPITestCase"
]
