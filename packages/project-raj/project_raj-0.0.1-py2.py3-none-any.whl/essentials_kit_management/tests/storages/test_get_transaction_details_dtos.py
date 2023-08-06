import pytest
import datetime
from freezegun import freeze_time
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import TransactionDetailsDto

@freeze_time("2020-05-17 20:22:46")
@pytest.mark.django_db
def test_get_transaction_details_dtos_returns_list_of_dtos(
        users, transactions):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    storage = StorageImplementation()
    expected_transaction_details_dtos = [
        TransactionDetailsDto(
            transaction_id=1,
            transaction_date=datetime.datetime(2020, 5, 17, 20, 22, 46),
            credit_amount=1000.0,
            debit_amount=0.0,
            verification_status='APPROVED',
            remarks='Snacks Form'
        ),
        TransactionDetailsDto(
            transaction_id=2,
            transaction_date=datetime.datetime(2020, 5, 17, 20, 22, 46),
            debit_amount=100.0, credit_amount=0.0, verification_status=None,
            remarks='Wallet'
        )
    ]
    
    #Act
    transaction_details_dtos = storage.get_transaction_details_dtos(
        user_id=user_id, limit=5, offset=0
    )
    
    #Assert
    assert transaction_details_dtos == expected_transaction_details_dtos
