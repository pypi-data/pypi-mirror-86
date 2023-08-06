"""
post form details with item ids by omit the previous created orders deletes ordered_items for those item_ids in order_items
"""

import json
from essentials_kit_management.utils.custom_test_utils import \
    create_complete_forms, CustomUtilsAPI
from essentials_kit_management.tests.factories.factories import \
    OrderItemFactory
from essentials_kit_management.models import OrderItem
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "item_details": [
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


class TestCase06PostFormDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase06PostFormDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )
        create_complete_forms()
        OrderItemFactory.create()

    def test_case(self):
        self.default_test_case()
        is_ordered_item_exists = OrderItem.objects.filter(item_id=1).exists()
        is_ordered_item_deleted = not is_ordered_item_exists
        self.assert_match_snapshot(
            name="is_ordered_item_deleted", value=is_ordered_item_deleted
        )
