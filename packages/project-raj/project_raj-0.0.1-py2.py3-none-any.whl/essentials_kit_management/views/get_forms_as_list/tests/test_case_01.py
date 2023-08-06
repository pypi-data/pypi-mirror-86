"""
get forms with offset and limit returns list of forms with pagenation
"""

import json
import datetime
from freezegun import freeze_time
from essentials_kit_management.utils.custom_test_utils import \
    create_complete_forms, create_users, CustomUtilsAPI
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {"offset": 0, "limit": 5},
        "header_params": {},
        "securities": {"user_oauth": {"tokenUrl": "localhost:8080/oauth2/token/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetFormsAsListAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        super(TestCase01GetFormsAsListAPITestCase, self).setupUser(
            username=username, password=password
        )
        create_users()
        create_complete_forms()

    @freeze_time(datetime.datetime(2020, 10, 9, 10, 2, 3))
    def test_case(self):
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="forms", value=response_content["forms"]
        )
