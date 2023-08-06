"""
Login with invalid password for username raises invalid username exception
"""

import json
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from essentials_kit_management.tests.factories.factories import UserFactory
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "username": "user_1",
    "password": "string"
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {},
        "body": REQUEST_BODY,
    },
}


class TestCase02LoginAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def test_case(self):
        UserFactory.create()
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="http_status_code", value=\
                response_content["http_status_code"]
        )
        self.assert_match_snapshot(
            name="res_status", value=response_content["res_status"]
        )
        self.assert_match_snapshot(
            name="response", value=response_content["response"]
        )
