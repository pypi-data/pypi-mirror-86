"""
get pay through details returns upi id to pay
"""

import json
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from essentials_kit_management.tests.factories.factories import \
    BankDetailsFactory
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"user_oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetPayThroughDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE
    
    def setupUser(self, username, password):
        super(TestCase01GetPayThroughDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )
        BankDetailsFactory.create()

    def test_case(self):
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="upi_id", value=response_content['upi_id']
        )
