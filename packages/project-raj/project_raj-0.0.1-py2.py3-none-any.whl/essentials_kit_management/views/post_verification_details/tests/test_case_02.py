"""
post verification details of payment creates transaction
"""

import json
import datetime
from freezegun import freeze_time
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from essentials_kit_management.models import Transaction
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "verification_details": {
        "amount": 100.0,
        "payment_transaction_id": "string",
        "transaction_type": "PHONE_PAY",
        "screenshot_url": "string"
    }
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["write"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase02PostVerificationDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase02PostVerificationDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )

    @freeze_time(datetime.datetime(2020, 6, 7, 9, 5, 4))
    def test_case(self):
        self.default_test_case()

        transaction = Transaction.objects.all().first()
        self.assert_match_snapshot(
            name="transaction_id", value=transaction.id
        )
        self.assert_match_snapshot(
            name="payment_transaction_id",
            value=transaction.payment_transaction_id
        )
        self.assert_match_snapshot(
            name="transaction_type", value=transaction.transaction_type
        )
        self.assert_match_snapshot(
            name="credit_amount", value=transaction.credit_amount
        )
        self.assert_match_snapshot(
            name="debit_amount", value=transaction.debit_amount
        )
        self.assert_match_snapshot(
            name="transaction_date", value=transaction.transaction_date
        )
        self.assert_match_snapshot(
            name="screenshot_url", value=transaction.screenshot_url
        )
        self.assert_match_snapshot(
            name="remarks", value=transaction.remarks
        )
        self.assert_match_snapshot(
            name="verification_status", value=transaction.verification_status
        )
        self.assert_match_snapshot(
            name="user_id", value=transaction.user_id
        )
