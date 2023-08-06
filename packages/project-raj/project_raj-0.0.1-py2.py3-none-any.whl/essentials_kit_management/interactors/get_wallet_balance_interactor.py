from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface


class GetWalletBalanceInteractor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage
    
    def get_wallet_balance_wrapper(self, user_id: int,
                                   presenter: PresenterInterface):
        wallet_balance = self.get_wallet_balance(user_id=user_id)
        return presenter.get_wallet_balance_response(
            wallet_balance=wallet_balance
        )

    def get_wallet_balance(self, user_id: int):
        wallet_balance = self.storage.get_wallet_balance(user_id=user_id)
        return wallet_balance
