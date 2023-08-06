from common.oauth2_storage import OAuth2SQLStorage
from essentials_kit_management.exceptions.exceptions \
    import InvalidPasswordException
from essentials_kit_management.interactors.storages.user_storage_interface \
    import UserStorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from common.oauth_user_auth_tokens_service \
    import OAuthUserAuthTokensService

class LoginInteractor:

    def __init__(
            self, user_storage: UserStorageInterface,
            oauth_storage: OAuth2SQLStorage,
            presenter: PresenterInterface):
        self.user_storage = user_storage
        self.presenter = presenter
        self.oauth_storage = oauth_storage

    def login_with_credentials(self, username: str, password: str):
        is_valid_username = \
            self.user_storage.validate_username(username=username)
        is_invalid_username = not is_valid_username
        if is_invalid_username:
            self.presenter.raise_invalid_username_exception()
            return

        try:
            user_id = \
                self.user_storage.get_user_id_for_valid_username_password(
                    username=username,
                    password=password
                )
        except InvalidPasswordException:
            self.presenter.raise_invalid_password_exception()
            return

        service = \
            OAuthUserAuthTokensService(oauth2_storage=self.oauth_storage)
        access_token_dto = service.create_user_auth_tokens(user_id=user_id)

        response = self.presenter.get_access_token_response(
            access_token_dto=access_token_dto
        )
        return response
