from typing import List
from abc import abstractmethod, ABC
from essentials_kit_management.interactors.storages.dtos \
    import TransactionDetailsDto
from essentials_kit_management.interactors.dtos \
    import PostVerificationDetailsDto


class StorageInterface(ABC):

    @abstractmethod
    def get_item_ids_from_db_if_given_ids_valid(
            self, item_ids: List[int]) -> List[int]:
        pass

    @abstractmethod
    def get_brand_ids_from_db_if_given_ids_valid(
            self, brand_ids: List[int]) -> List[int]:
        pass

    @abstractmethod
    def get_wallet_balance(self, user_id: int) -> int:
        pass

    @abstractmethod
    def get_transaction_details_dtos(self, user_id: int, offset: int,
                                     limit: int
                                     ) -> List[TransactionDetailsDto]:
        pass

    @abstractmethod
    def create_transaction_request(
            self, user_id: int,
            verification_details_dto: PostVerificationDetailsDto):
        pass

    @abstractmethod
    def get_upi_id(self) -> str:
        pass

    @abstractmethod
    def get_transactions_dtos(self, user_id: int,
                              offset: int, limit: int
                              ) -> List[TransactionDetailsDto]:
        pass