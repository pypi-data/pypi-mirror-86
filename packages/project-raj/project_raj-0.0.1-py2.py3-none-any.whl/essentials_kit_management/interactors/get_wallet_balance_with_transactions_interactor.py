from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.get_wallet_balance_interactor \
    import GetWalletBalanceInteractor
from essentials_kit_management.interactors.\
    get_transactions_details_interactor import \
    GetTransactionsDetailsInteractor
from essentials_kit_management.interactors.storages.dtos \
    import WalletTransactionDetailsDto


class GetWalletBalanceWithTransactionsInteractor:
    def __init__(
            self, storage: StorageInterface):
        self.storage = storage

    def get_wallet_balance_with_transactions_wrapper(
            self, user_id: int, offset: int,
            limit: int, presenter: PresenterInterface
    ):
        wallet_transactions_dto = \
            self.get_wallet_balance_with_transactions(
                user_id=user_id, offset=offset, limit=limit
            )
        return presenter.get_wallet_balance_with_transactions_response(
            wallet_balance_with_transactions_dto=wallet_transactions_dto
        )

    def get_wallet_balance_with_transactions(self, user_id: int,
                                             offset: int, limit: int):
        
        wallet_balance_interactor = GetWalletBalanceInteractor(self.storage)
        transactions_details_interactor = \
            GetTransactionsDetailsInteractor(self.storage)
        
        wallet_balance = \
            wallet_balance_interactor.get_wallet_balance(user_id=user_id)
        transaction_details_dtos = \
            transactions_details_interactor.get_transactions_details(
                user_id=user_id, offset=offset, limit=limit
            )

        wallet_transactions_dto = WalletTransactionDetailsDto(
            wallet_balance=wallet_balance,
            transaction_details_dtos=transaction_details_dtos
        )

        return wallet_transactions_dto
