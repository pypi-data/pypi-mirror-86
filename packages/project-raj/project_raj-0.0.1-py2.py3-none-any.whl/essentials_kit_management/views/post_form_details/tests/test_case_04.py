"""
post form details creates order items of form for the user
"""

import json
from essentials_kit_management.utils.custom_test_utils import \
    create_complete_forms, CustomUtilsAPI
from essentials_kit_management.models import OrderItem
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


class TestCase04PostFormDetailsAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase04PostFormDetailsAPITestCase, self).setupUser(
            username=username, password=password
        )
        create_complete_forms()

    def test_case(self):
        self.default_test_case()
        ordered_item = OrderItem.objects.filter(id=1).first()
        self.assert_match_snapshot(
            name=f"user_id_for_item_{ordered_item.item_id}",
            value=ordered_item.ordered_quantity
        )
        self.assert_match_snapshot(
            name=f"item_id_{ordered_item.item_id}",
            value=ordered_item.item_id
        )
        self.assert_match_snapshot(
            name=f"brand_id_for_item_{ordered_item.item_id}",
            value=ordered_item.brand_id
        )
        self.assert_match_snapshot(
            name=f"ordered_quantity_for_item_{ordered_item.item_id}",
            value=ordered_item.ordered_quantity
        )
        self.assert_match_snapshot(
            name=f"delivered_quantity_for_item_{ordered_item.item_id}",
            value=ordered_item.delivered_quantity
        )
        self.assert_match_snapshot(
            name=\
                f"is_out_of_stock_for_item_{ordered_item.item_id}",
            value=ordered_item.is_out_of_stock
        )

