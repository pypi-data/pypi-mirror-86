import pytest
from essentials_kit_management.storages.user_storage_implementation \
    import UserStorageImplementation


@pytest.mark.django_db
def test_validate_access_token_with_valid_access_token_returns_true(
        access_tokens):
    #Arrange
    access_token="jsdfbjherbfgvjb"
    user_storage = UserStorageImplementation()

    #Act
    is_valid_access_token = \
        user_storage.validate_access_token(access_token=access_token)

    #Assert
    assert is_valid_access_token is True


@pytest.mark.django_db
def test_validate_access_token_with_invalid_access_token_returns_false(
        access_tokens):
    #Arrange
    invalid_access_token="jsdfbjherbfgsdkfjbdsjk"
    user_storage = UserStorageImplementation()

    #Act
    is_valid_access_token = user_storage.validate_access_token(
        access_token=invalid_access_token
    )

    #Assert
    assert is_valid_access_token is False
