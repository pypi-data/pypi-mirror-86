from typing import Optional
from abc import abstractmethod, ABC


class UserStorageInterface(ABC):

    @abstractmethod
    def validate_username(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_user_id_for_valid_username_password(
            self, username: str, password: str) -> Optional[int]:
        pass

    @abstractmethod
    def validate_access_token(self, access_token: str) -> bool:
        pass

    @abstractmethod
    def delete_access_token(self, access_token: str):
        pass
