import pytest
from oauth2_provider.models import AccessToken
from essentials_kit_management.storages.user_storage_implementation \
    import UserStorageImplementation


@pytest.mark.django_db
def test_delete_access_token_with_valid_access_deletes_in_db(
        access_tokens):
    #Arrange
    access_token="jsdfbjherbfgvjb"
    user_storage = UserStorageImplementation()

    #Act
    user_storage.delete_access_token(access_token=access_token)

    #Assert
    is_access_token_exists = \
        AccessToken.objects.filter(token=access_token).exists()
    
    assert is_access_token_exists is False
