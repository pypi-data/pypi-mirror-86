"""
logout will deletes the user access token
"""

from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from oauth2_provider.models import AccessToken
from essentials_kit_management.utils.custom_test_utils import create_users
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
    {}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["delete"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01LogoutAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE
    
    def setupUser(self, username, password):
        super(TestCase01LogoutAPITestCase, self).setupUser(
            username=username, password=password
        )

    def test_case(self):
        self.default_test_case()
        is_access_token_exists = \
            AccessToken.objects.filter(user_id=1).exists()
        is_user_successfully_logged_out = not is_access_token_exists
        self.assert_match_snapshot(
            name="is_user_successfully_logged_out",
            value=is_user_successfully_logged_out
        )
