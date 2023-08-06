from essentials_kit_management.interactors.storages.user_storage_interface \
    import UserStorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface


class LogoutInteractor:

    def __init__(
            self, user_storage: UserStorageInterface,
            presenter: PresenterInterface):
        self.user_storage = user_storage
        self.presenter = presenter

    def logout(self, access_token: str):
        is_valid_access_token = \
            self.user_storage.validate_access_token(access_token=access_token)
        is_invalid_access_token = not is_valid_access_token

        if is_invalid_access_token:
            self.presenter.raise_invalid_access_token_exception()
            return

        self.user_storage.delete_access_token(access_token=access_token)
        self.presenter.logout_response()

        return
