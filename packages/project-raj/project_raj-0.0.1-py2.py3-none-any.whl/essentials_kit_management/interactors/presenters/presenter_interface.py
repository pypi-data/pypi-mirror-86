from abc import ABC
from typing import Dict
from abc import abstractmethod
from common.dtos import UserAuthTokensDTO
from essentials_kit_management.interactors.storages.dtos \
    import CompleteFormsDetailsDto, FormsListMetricsDto, FormMetricsDto, \
    CompleteFormDetailsDto, OrderDetailsOfFormDto, \
    WalletTransactionDetailsDto, TransactionDetailsDto


class PresenterInterface(ABC):

    @abstractmethod
    def raise_invalid_username_exception(self):
        pass

    @abstractmethod
    def raise_invalid_form_exception(self):
        pass

    @abstractmethod
    def raise_invalid_password_exception(self):
        pass

    @abstractmethod
    def raise_invalid_brand_id_exception(self):
        pass

    @abstractmethod
    def raise_invalid_item_id_exception(self):
        pass

    @abstractmethod
    def get_access_token_response(self, access_token_dto: UserAuthTokensDTO):
        pass

    @abstractmethod
    def get_forms_details_response(
            self, forms_details: CompleteFormsDetailsDto,
            forms_list_metrics_dtos: FormsListMetricsDto):
        pass

    @abstractmethod
    def get_form_details_response(
            self, complete_form_details_dto: CompleteFormDetailsDto,
            form_metrics_dto: FormMetricsDto):
        pass

    @abstractmethod
    def post_form_details_response(self):
        pass

    @abstractmethod
    def get_order_details_of_form_response(
            self, ordered_details_of_form_dto: OrderDetailsOfFormDto):
        pass

    @abstractmethod
    def get_wallet_transaction_details_response(
            self, wallet_transactions_dto: WalletTransactionDetailsDto):
        pass

    @abstractmethod
    def post_verification_details_response(self):
        pass

    @abstractmethod
    def get_pay_through_details_response(self, upi_id: str):
        pass

    @abstractmethod
    def logout_response(self):
        pass

    @abstractmethod
    def raise_invalid_value_exception(self):
        pass

    @abstractmethod
    def raise_invalid_access_token_exception(self):
        pass

    @abstractmethod
    def get_wallet_balance_response(self, wallet_balance: float):
        pass

    @abstractmethod
    def get_transaction_details_response(
            self, transaction_details_dtos: TransactionDetailsDto):
        pass

    @abstractmethod
    def get_wallet_balance_with_transactions_response(
            self,
            wallet_balance_with_transactions_dto: WalletTransactionDetailsDto
    ):
        pass
