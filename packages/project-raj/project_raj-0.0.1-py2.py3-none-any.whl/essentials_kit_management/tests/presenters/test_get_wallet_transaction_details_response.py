import datetime
from freezegun import freeze_time
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.storages.dtos \
    import TransactionDetailsDto, WalletTransactionDetailsDto


@freeze_time("2020-05-17")
def test_get_wallet_transactions_details_response_returns_total_wallet_details():
    #Assert
    json_presenter = PresenterImplementation()
    expected_wallet_transaction_details = {
        'transaction_details': [
            {
                'remarks': 'Snacks Form',
                'credit_amount': 1000.0,
                'debit_amount': 0.0,
                'transaction_date': '17 May 2020',
                'transaction_id': 1,
                'verification_status': 'APPROVED'
            },
            {
                'remarks': 'Wallet',
                'credit_amount': 0.0,
                'debit_amount': 100.0,
                'transaction_date': '17 May 2020',
                'transaction_id': 2,
                'verification_status': None
            }
        ],
        'wallet_balance': 10000
    }


    transaction_details_dtos = [
        TransactionDetailsDto(
            transaction_id=1,
            transaction_date=datetime.datetime(2020, 5, 17, 20, 22, 46),
            credit_amount=1000.0,
            debit_amount=0.0,
            verification_status='APPROVED',
            remarks='Snacks Form'
        ),
        TransactionDetailsDto(
            transaction_id=2,
            transaction_date=datetime.datetime(2020, 5, 17, 20, 22, 46),
            debit_amount=100.0, verification_status=None,credit_amount=0,
            remarks='Wallet'
        )
    ]

    wallet_transactions_details_dto = WalletTransactionDetailsDto(
        wallet_balance=10000,
        transaction_details_dtos=transaction_details_dtos
    )


    #Act
    wallet_transactions_details = \
        json_presenter.get_wallet_transaction_details_response(
            wallet_transactions_dto=wallet_transactions_details_dto
        )

    #Assert
    assert wallet_transactions_details == expected_wallet_transaction_details
