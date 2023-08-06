from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface


class GetTransactionsDetailsInteractor:
    def __init__(
            self, storage: StorageInterface):
        self.storage = storage

    def get_transactions_details_wrapper(self, user_id: int,
                                         limit: int, offset: int,
                                         presenter: PresenterInterface):
        transaction_details_dtos = self.get_transactions_details(
             user_id=user_id, offset=offset, limit=limit
        )

        presenter.get_transaction_details_response(
            transaction_details_dtos=transaction_details_dtos
        )

    def get_transactions_details(self, user_id: int, offset: int, limit: int):

        transaction_details_dtos = self.storage.get_transaction_details_dtos(
            user_id=user_id, offset=offset, limit=limit
        )
        return transaction_details_dtos
