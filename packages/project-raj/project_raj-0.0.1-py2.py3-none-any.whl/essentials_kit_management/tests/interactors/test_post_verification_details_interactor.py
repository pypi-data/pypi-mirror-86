import pytest
from mock import create_autospec
from django_swagger_utils.drf_server.exceptions import BadRequest
from essentials_kit_management.interactors.\
    post_verification_details_interactor \
    import PostVerificationDetailsInteractor
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface
from essentials_kit_management.interactors.dtos \
    import PostVerificationDetailsDto
from essentials_kit_management.constants.enums import TransactionTypeEnum


def test_post_verification_details_with_valid_data_creates_verification_details():
    #Arrange
    user_id = 1
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostVerificationDetailsInteractor(
        storage=storage, presenter=presenter
    )

    verification_details = {
        "amount": 10000,
        "payment_transaction_id": 1234567884,
        "transaction_type": TransactionTypeEnum.PHONE_PAY.value,
        "screenshot_url": "https://google.com"
    }

    verification_details_dto = PostVerificationDetailsDto(
        amount=10000,
        payment_transaction_id=1234567884,
        transaction_type=TransactionTypeEnum.PHONE_PAY.value,
        screenshot_url="https://google.com"
    )

    #Act
    interactor.post_verification_details(
        user_id=user_id, verification_details=verification_details
    )

    #Assert
    storage.create_transaction_request.assert_called_once_with(
        user_id=user_id, verification_details_dto=verification_details_dto
    )
    presenter.post_verification_details_response.assert_called_once()


def test_post_verification_details_with_negative_amount_raises_exception():
    #Arrange
    user_id = 1
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostVerificationDetailsInteractor(
        storage=storage, presenter=presenter
    )

    verification_details = {
        "amount": -100,
    }
    presenter.raise_invalid_value_exception.side_effect = BadRequest

    #Act
    with pytest.raises(BadRequest):
        interactor.post_verification_details(
            user_id=user_id, verification_details=verification_details
        )

    #Assert
    presenter.raise_invalid_value_exception.assert_called_once()
