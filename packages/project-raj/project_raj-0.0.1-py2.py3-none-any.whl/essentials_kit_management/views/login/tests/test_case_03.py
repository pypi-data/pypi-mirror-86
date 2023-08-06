"""
Login with username and password returns
"""

import json
from unittest.mock import patch
from essentials_kit_management.utils.custom_test_utils import CustomUtilsAPI
from common.dtos import UserAuthTokensDTO
from essentials_kit_management.tests.factories.factories import UserFactory
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "username": "user_1",
    "password": "rajesh"
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {},
        "body": REQUEST_BODY,
    },
}


class TestCase02LoginAPITestCase(CustomUtilsAPI):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    @patch(
        'common.oauth_user_auth_tokens_service.OAuthUserAuthTokensService.create_user_auth_tokens'
    )
    def test_case(self, mock_create_user_auth_tokens):
        mock_output = UserAuthTokensDTO(
            access_token='j3nu3SVLFBwl578WPeoJh3zed0YLjO',
            expires_in='2337-05-18 05:36:34.506841',
            refresh_token='EvEu5Za9Z3bkQrNFgsSaYzPCOXw4Eq',
            user_id=1
        )
        UserFactory.create()
        mock_create_user_auth_tokens.return_value = mock_output
        response = self.default_test_case()
        response_content = json.loads(response.content)
        self.assert_match_snapshot(
            name="user_id", value=response_content["user_id"]
        )
        self.assert_match_snapshot(
            name="access_token", value=response_content["access_token"]
        )
        self.assert_match_snapshot(
            name="expires_in", value=response_content["expires_in"]
        )
        self.assert_match_snapshot(
            name="refresh_token", value=response_content["refresh_token"]
        )
