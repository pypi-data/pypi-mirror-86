import pytest
from mock import create_autospec, patch
from django_swagger_utils.drf_server.exceptions import Unauthorized
from common.dtos import UserAuthTokensDTO
from common.oauth_user_auth_tokens_service import OAuthUserAuthTokensService
from common.oauth2_storage import OAuth2SQLStorage
from essentials_kit_management.interactors.login_interactor \
    import LoginInteractor
from essentials_kit_management.interactors.storages.user_storage_interface \
    import UserStorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface
from essentials_kit_management.exceptions.exceptions \
    import InvalidPasswordException


def test_login_interactor_with_valid_credentials_creates_new_access_token():
    #Arrange
    user_id = 1
    username = "9032751617"
    password = "admin123"
    access_token = "1ke3ue3ijkbdfsfdke"
    time_in_sec = 10000000
    refresh_token = "hsbfdhjbsjkfb"

    user_storage = create_autospec(UserStorageInterface)
    presenter = create_autospec(PresenterInterface)
    oauth_storage = create_autospec(OAuth2SQLStorage)
    interactor = LoginInteractor(
        user_storage=user_storage,
        presenter=presenter,
        oauth_storage=oauth_storage
    )

    mock_access_token_dto = UserAuthTokensDTO(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=time_in_sec
    )

    #ACT
    with patch.object(
            OAuthUserAuthTokensService, 'create_user_auth_tokens',
            return_value=mock_access_token_dto):
        interactor.login_with_credentials(
            username=username, password=password
        )

    #Assert
    user_storage.validate_username.assert_called_once_with(username=username)
    user_storage.get_user_id_for_valid_username_password.\
        assert_called_once_with(username=username, password=password)
    presenter.get_access_token_response.assert_called_once_with(
        access_token_dto=mock_access_token_dto
    )


def test_login_interactor_with_invalid_username_raises_invalid_username_exception():
    #Arrange
    invalid_username = "Rajesh"
    password = "admin123"
    user_storage = create_autospec(UserStorageInterface)
    presenter = create_autospec(PresenterInterface)
    oauth_storage = create_autospec(OAuth2SQLStorage)
    interactor = LoginInteractor(
        user_storage=user_storage,
        presenter=presenter,
        oauth_storage=oauth_storage
    )
    user_storage.validate_username.return_value = False
    presenter.raise_invalid_username_exception.side_effect = Unauthorized

    #Act
    with pytest.raises(Unauthorized):
        interactor.login_with_credentials(
            username=invalid_username,
            password=password
        )

    #Assert
    user_storage.validate_username.assert_called_once_with(
        username=invalid_username
    )
    presenter.raise_invalid_username_exception.assert_called_once()


def test_login_interactor_with_invalid_password_for_username_raises_invalid_password_exception():
    #Arrange
    username = "Rajesh"
    invalid_password = "admin123"
    user_storage = create_autospec(UserStorageInterface)
    presenter = create_autospec(PresenterInterface)
    oauth_storage = create_autospec(OAuth2SQLStorage)
    interactor = LoginInteractor(
        user_storage=user_storage,
        presenter=presenter,
        oauth_storage=oauth_storage
    )
    user_storage.validate_username.return_value = True
    user_storage.get_user_id_for_valid_username_password.side_effect = \
        InvalidPasswordException
    presenter.raise_invalid_password_exception.side_effect = Unauthorized

    #Act
    with pytest.raises(Unauthorized):
        interactor.login_with_credentials(
            username=username,
            password=invalid_password
        )

    #Assert
    user_storage.validate_username.assert_called_once_with(
        username=username
    )
    user_storage.get_user_id_for_valid_username_password.\
        assert_called_once_with(username=username, password=invalid_password)
    presenter.raise_invalid_password_exception.assert_called_once()
