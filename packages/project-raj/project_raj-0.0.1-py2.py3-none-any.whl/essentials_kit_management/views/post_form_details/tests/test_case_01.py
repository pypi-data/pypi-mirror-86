"""
post form details with invalid form id raises invalid form exception
"""

import json
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "item_details": [
        {
            "item_id": 1,
            "brand_details": {
                "brand_id": 1
            },
            "ordered_quantity": 1
        }
    ]
}
"""

TEST_CASE = {
    "request": {
        "path_params": {"form_id": 1},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["write", "update"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01PostFormDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase01PostFormDetailsAPITestCase, self).setupUser(
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
