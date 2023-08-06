"""
Get form details with invalid form id raises Invalid Form exception
"""

import json
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {"form_id": 1},
        "query_params": {},
        "header_params": {},
        "securities": {"user_oauth": {"tokenUrl": "localhost:8080/oauth2/token/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetFormDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase01GetFormDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )

    def test_case(self):
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
