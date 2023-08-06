import pytest
from essentials_kit_management.storages import UserStorageImplementation
from essentials_kit_management.exceptions.exceptions \
    import InvalidPasswordException


@pytest.mark.django_db
def test_get_user_id_for_valid_username_password_with_invalid_password_raise_exception(users):
    #Arrange
    username = "Rajesh"
    invalid_password = "admin1243"
    user_storage = UserStorageImplementation()

    #Assert
    with pytest.raises(InvalidPasswordException):
        user_storage.get_user_id_for_valid_username_password(
            username=username, password=invalid_password
        )

'''
@pytest.mark.django_db
def test_get_user_id_for_valid_username_password_with_valid_password_returns_user_id(users):
    #Arrange
    username = "Rajesh"
    password = "admin1234"
    expected_user_id = 1
    user_storage = UserStorageImplementation()

    #Act
    user_id = user_storage.get_user_id_for_valid_username_password(
        username=username, password=password
    )

    #Assert
    assert user_id == expected_user_id
'''