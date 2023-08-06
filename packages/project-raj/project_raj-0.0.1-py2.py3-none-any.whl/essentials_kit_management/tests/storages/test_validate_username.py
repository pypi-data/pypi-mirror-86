import pytest
from essentials_kit_management.storages import UserStorageImplementation


@pytest.mark.django_db
def test_validate_username_for_valid_username_returns_true(users):
    #Arrange
    username = "Rajesh"
    user_storage = UserStorageImplementation()

    #Act
    is_valid_username = user_storage.validate_username(username=username)

    #Assert
    assert is_valid_username is True


@pytest.mark.django_db
def test_validate_username_for_invalid_username_returns_false(users):
    #Arrange
    invalid_username = "Yaswanth"
    user_storage = UserStorageImplementation()

    #Act
    is_valid_username = \
        user_storage.validate_username(username=invalid_username)

    #Assert
    assert is_valid_username is False
