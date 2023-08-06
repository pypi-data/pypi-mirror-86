from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.storages.dtos \
    import WalletTransactionDetailsDto


class GetWalletTransactionsDetailsInteractor:
    def __init__(
            self, storage: StorageInterface, presenter: PresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def get_wallet_transactions_details(self, user_id: int,
                                        offset: int, limit: int):
        wallet_balance = self.storage.get_wallet_balance(user_id=user_id)
        transaction_details_dtos = \
            self.storage.get_transaction_details_dtos(
                user_id=user_id, offset=offset, limit=limit
            )

        wallet_transactions_dto = WalletTransactionDetailsDto(
            wallet_balance=wallet_balance,
            transaction_details_dtos=transaction_details_dtos
        )

        wallet_transactions_details = \
            self.presenter.get_wallet_transaction_details_response(
                wallet_transactions_dto=wallet_transactions_dto
            )
        return wallet_transactions_details
