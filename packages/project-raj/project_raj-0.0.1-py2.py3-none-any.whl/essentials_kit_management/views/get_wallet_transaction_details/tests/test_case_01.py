"""
get wallet transaction details returns wallet balance and transaction details
"""

import json
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from essentials_kit_management.tests.factories.factories import \
    TransactionFactory
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """/wallet_

"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {"offset": 0, "limit": 5},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetWalletTransactionDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase01GetWalletTransactionDetailsAPITestCase, self)\
            .setupUser(username=username, password=password)
        TransactionFactory.create_batch(size=30)

    def test_case(self):
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="transaction_details",
            value=response_content["transaction_details"]
        )
        self.assert_match_snapshot(
            name="wallet_balance", value="wallet_balance"
        )
