import pytest
from mock import create_autospec
from django_swagger_utils.drf_server.exceptions import Unauthorized
from essentials_kit_management.interactors.logout_interactor \
    import LogoutInteractor
from essentials_kit_management.interactors.storages.user_storage_interface \
    import UserStorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface


def test_logout_interactor_with_invalid_access_token_raises_exception():
    #Arrane
    access_token = "akufiuwebfkjkrnfgkjvndfkj"
    user_storage = create_autospec(UserStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = LogoutInteractor(
        user_storage=user_storage, presenter=presenter
    )
    user_storage.validate_access_token.return_value = False
    presenter.raise_invalid_access_token_exception.side_effect = Unauthorized

    #Act
    with  pytest.raises(Unauthorized):
        interactor.logout(access_token=access_token)

    #Assert
    user_storage.validate_access_token.assert_called_once_with(
        access_token=access_token
    )
    presenter.raise_invalid_access_token_exception.assert_called_once()


def test_logout_interactor_with_valid_access_token_deletes_access_token():
    #Arrane
    access_token = "akufiuwebfkjkrnfgkjvndfkj"
    user_storage = create_autospec(UserStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = LogoutInteractor(
        user_storage=user_storage, presenter=presenter
    )
    user_storage.validate_access_token.return_value = True

    #Act
    interactor.logout(access_token=access_token)

    #Assert
    user_storage.validate_access_token.assert_called_once_with(
        access_token=access_token
    )
    user_storage.delete_access_token.assert_called_once_with(
        access_token=access_token
    )
    presenter.logout_response.assert_called_once()
