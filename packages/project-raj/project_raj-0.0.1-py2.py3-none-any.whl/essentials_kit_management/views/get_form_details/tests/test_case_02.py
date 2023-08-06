"""
Get form details returns form details
"""

import json
from essentials_kit_management.utils.custom_test_utils import \
    CustomUtilsAPI, create_complete_forms
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {"form_id": 10},
        "query_params": {},
        "header_params": {},
        "securities": {"user_oauth": {"tokenUrl": "localhost:8080/oauth2/token/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase02GetFormDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase02GetFormDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )
        create_complete_forms()


    def test_case(self):
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="form_id", value=response_content["form_id"]
        )
        self.assert_match_snapshot(
            name="form_name", value=response_content["form_name"]
        )
        self.assert_match_snapshot(
            name="form_description",
            value=response_content["form_description"]
        )
        self.assert_match_snapshot(
            name="close_date", value=response_content["close_date"]
        )
        self.assert_match_snapshot(
            name="total_cost", value=response_content["total_cost"]
        )
        self.assert_match_snapshot(
            name="total_items", value=response_content["total_items"]
        )
        self.assert_match_snapshot(
            name="sections", value=response_content["sections"]
        )
