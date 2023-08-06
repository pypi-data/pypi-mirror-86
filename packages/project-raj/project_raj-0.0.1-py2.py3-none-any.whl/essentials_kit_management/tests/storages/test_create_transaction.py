import pytest
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.models import Transaction
from essentials_kit_management.constants.enums import TransactionTypeEnum
from essentials_kit_management.interactors.dtos \
    import PostVerificationDetailsDto


@pytest.mark.django_db
def test_create_transaction_with_valid_data_creates_new_transaction_in_db(
        users):
    #Arrange
    user_id = 1
    storage = StorageImplementation()
    expected_transaction_id = 1
    credit_amount = 10000.0
    debit_amount = 0
    expected_payment_transaction_id = "1234567884"
    expected_transaction_type = TransactionTypeEnum.PHONE_PAY.value
    expected_screenshot_url = "https://google.com"

    verification_details_dto = PostVerificationDetailsDto(
        amount=10000.0,
        payment_transaction_id="1234567884",
        transaction_type=TransactionTypeEnum.PHONE_PAY.value,
        screenshot_url="https://google.com"
    )

    #Act
    storage.create_transaction_request(
        user_id=user_id, verification_details_dto=verification_details_dto
    )

    #Assert
    transaction = Transaction.objects.get(id=expected_transaction_id)

    assert transaction.id == expected_transaction_id
    assert transaction.credit_amount == credit_amount
    assert transaction.debit_amount == debit_amount
    assert transaction.payment_transaction_id == \
        expected_payment_transaction_id
    assert transaction.transaction_type == expected_transaction_type
    assert transaction.screenshot_url == expected_screenshot_url
