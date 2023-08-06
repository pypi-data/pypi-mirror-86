import pytest
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation


@pytest.mark.django_db
def test_get_wallet_balance_returns_wallet_balance(users, transactions):
    #Arrange
    user_id = 1
    storage = StorageImplementation()
    expected_wallet_balance = 900.0

    #Act
    wallet_balance = storage.get_wallet_balance(user_id=user_id)

    #Assert
    assert wallet_balance == expected_wallet_balance


@pytest.mark.django_db
def test_get_wallet_balance_returns_zero_as_default_wallet_balance(
        users, transactions):
    #Arrange
    user_id = 2
    expected_wallet_balance = 0
    storage = StorageImplementation()

    #Act
    wallet_balance = storage.get_wallet_balance(user_id=user_id)

    #Assert
    assert wallet_balance == expected_wallet_balance
