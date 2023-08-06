from typing import List
from django.db.models import Sum, Q
from essentials_kit_management.models \
    import Brand, Item, Transaction, BankDetails
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.storages.dtos \
    import TransactionDetailsDto
from essentials_kit_management.interactors.dtos \
    import PostVerificationDetailsDto
from essentials_kit_management.constants.enums import VerificationChoicesEnum


class StorageImplementation(StorageInterface):

    def get_item_ids_from_db_if_given_ids_valid(
            self, item_ids: List[int]) -> List[int]:
        item_ids_query_set = \
            Item.objects.filter(id__in=item_ids).values_list('id', flat=True)
        item_ids_in_db = list(item_ids_query_set)
        return item_ids_in_db

    def get_brand_ids_from_db_if_given_ids_valid(
            self, brand_ids: List[int]) -> List[int]:
        brand_ids_query_set = \
            Brand.objects.filter(
                id__in=brand_ids
            ).values_list('id', flat=True)
        brand_ids_in_db = list(brand_ids_query_set)
        return brand_ids_in_db

    def get_wallet_balance(self, user_id: int):
        balance_dict = Transaction.objects.filter(user_id=user_id).exclude(
            Q(verification_status=VerificationChoicesEnum.PENDING.value) |
            Q(verification_status=VerificationChoicesEnum.DECLINED.value)
        ).aggregate(balance=Sum('credit_amount') - Sum('debit_amount'))

        wallet_balance = balance_dict['balance']
        if wallet_balance:
            return wallet_balance
        wallet_balance = 0.0
        return wallet_balance

    def get_transaction_details_dtos(self, user_id: int,
                                     offset: int, limit: int
                                     ) -> List[TransactionDetailsDto]:
        transactions = Transaction.objects.filter(
            user_id=user_id
        )[offset:offset + limit]
        transaction_details_dtos = \
            self._convert_transactions_to_dtos(transactions)
        return transaction_details_dtos

    def create_transaction_request(
            self, user_id: int,
            verification_details_dto: PostVerificationDetailsDto):
        amount = verification_details_dto.amount
        payment_transaction_id = \
            verification_details_dto.payment_transaction_id
        transaction_type = verification_details_dto.transaction_type
        screenshot_url = verification_details_dto.screenshot_url

        Transaction.objects.create(
            user_id=user_id, credit_amount=amount,
            payment_transaction_id=payment_transaction_id,
            transaction_type=transaction_type, screenshot_url=screenshot_url
        )
        return

    def get_upi_id(self) -> str:
        upi_id_in_queryset = BankDetails.objects.all().values_list(
            'upi_id', flat=True
        )
        upi_id = upi_id_in_queryset.first()
        return upi_id

    @staticmethod
    def _convert_transactions_to_dtos(transactions):
        transaction_details_dtos = [
            TransactionDetailsDto(
                transaction_id=transaction.id,
                transaction_date=transaction.transaction_date,
                credit_amount=transaction.credit_amount,
                debit_amount=transaction.debit_amount,
                verification_status=transaction.verification_status,
                remarks=transaction.remarks
            )
            for transaction in transactions
        ]
        return transaction_details_dtos

    def get_transactions_dtos(self, user_id: int,
                                     offset: int, limit: int
                                     ) -> List[TransactionDetailsDto]:
        pass
