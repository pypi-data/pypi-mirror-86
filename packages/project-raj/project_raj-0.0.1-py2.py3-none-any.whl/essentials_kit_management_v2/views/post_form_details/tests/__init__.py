# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management_v2"
OPERATION_NAME = "post_form_details"
REQUEST_METHOD = "post"
URL_SUFFIX = "forms/{form_id}/v1/"

from .test_case_01 import TestCase01PostFormDetailsAPITestCase

__all__ = [
    "TestCase01PostFormDetailsAPITestCase"
]
