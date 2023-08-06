from typing import Optional
from oauth2_provider.models import AccessToken
from essentials_kit_management.exceptions.exceptions \
    import InvalidPasswordException
from essentials_kit_management.interactors.storages.user_storage_interface \
    import UserStorageInterface
from essentials_kit_management.models import User


class UserStorageImplementation(UserStorageInterface):

    def validate_username(self, username: str) -> bool:
        is_valid_username = User.objects.filter(username=username).exists()
        return is_valid_username

    def get_user_id_for_valid_username_password(
            self, username: str, password: str) -> Optional[int]:
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            raise InvalidPasswordException
        return user.id

    def validate_access_token(self, access_token: str) -> bool:
        is_valid_access_token = \
            AccessToken.objects.filter(token=access_token).exists()
        return is_valid_access_token

    def delete_access_token(self, access_token: str):
        AccessToken.objects.get(token=access_token).delete()
        return
