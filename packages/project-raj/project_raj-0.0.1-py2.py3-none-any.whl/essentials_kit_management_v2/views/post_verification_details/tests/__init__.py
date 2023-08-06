# pylint: disable=wrong-import-position

APP_NAME = "essentials_kit_management_v2"
OPERATION_NAME = "post_verification_details"
REQUEST_METHOD = "post"
URL_SUFFIX = "transactions/verification_details/v1/"

from .test_case_01 import TestCase01PostVerificationDetailsAPITestCase

__all__ = [
    "TestCase01PostVerificationDetailsAPITestCase"
]
