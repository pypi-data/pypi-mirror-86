"""
Get order details of a form returns ordered items
"""

import json
from django_swagger_utils.utils.test import CustomAPITestCase
from essentials_kit_management.utils.custom_test_utils import \
    create_complete_forms, CustomUtilsAPI
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {"form_id": 1},
        "query_params": {},
        "header_params": {},
        "securities": {"user_oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetOrderDetailsOfFormAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase01GetOrderDetailsOfFormAPITestCase, self).setupUser(
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
            name="ordered_details", value=response_content["order_details"]
        )
        self.assert_match_snapshot(
            name="cost_incurred",
            value=response_content["total_cost_incurred"]
        )
        self.assert_match_snapshot(
            name="total_items_count",
            value=response_content["total_items_count"]
        )
        self.assert_match_snapshot(
            name="received_items_count",
            value=response_content["total_received_items_count"]
        )
