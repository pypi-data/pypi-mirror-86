from mock import create_autospec
from essentials_kit_management.interactors.\
    get_wallet_transactions_details_interactor \
    import GetWalletTransactionsDetailsInteractor
from essentials_kit_management.interactors.storages.dtos \
    import WalletTransactionDetailsDto, TransactionDetailsDto
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface
from essentials_kit_management.constants.enums import VerificationChoicesEnum


def test_get_wallet_transactions_details_returns_dto():
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetWalletTransactionsDetailsInteractor(
        storage=storage, presenter=presenter
    )

    mock_wallet_balance = 1000
    mock_transaction_dtos = [
        TransactionDetailsDto(
            transaction_id=1,
            transaction_date="2020-05-02",
            credit_amount=10000,
            debit_amount=0,
            verification_status=VerificationChoicesEnum.APPROVED.value,
            remarks="Wallet"
        )
    ]
    mock_presenter_response = {
        "wallet_balance": 0,
        "transaction_details": [
            {
                "transaction_id": 0,
                "transaction_date": "2020-06-02",
                "transaction_amount": 0,
                "verification_status": VerificationChoicesEnum.APPROVED.value,
                "remarks": "string"
            }
        ]
    }

    expected_wallet_transactions_dto = WalletTransactionDetailsDto(
        wallet_balance=mock_wallet_balance,
        transaction_details_dtos=mock_transaction_dtos
    )

    storage.get_wallet_balance.return_value = mock_wallet_balance
    storage.get_transaction_details_dtos.return_value = mock_transaction_dtos
    presenter.get_wallet_transaction_details_response.return_value = \
        mock_presenter_response

    #Act
    wallet_transactions_details = interactor.get_wallet_transactions_details(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert wallet_transactions_details == mock_presenter_response
    storage.get_wallet_balance.assert_called_once_with(user_id=user_id)
    storage.get_transaction_details_dtos.assert_called_once_with(
        user_id=user_id, limit=5, offset=0
    )
    presenter.get_wallet_transaction_details_response.assert_called_once_with(
        wallet_transactions_dto=expected_wallet_transactions_dto
    )


def test_get_wallet_transactions_details_with_no_transactions_returns_empty_transaction_dtos():
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetWalletTransactionsDetailsInteractor(
        storage=storage, presenter=presenter
    )

    mock_wallet_balance = 1000
    mock_transaction_dtos = []

    mock_presenter_response = {
        "wallet_balance": 0,
        "transaction_details": []
    }

    expected_wallet_transactions_dto = WalletTransactionDetailsDto(
        wallet_balance=mock_wallet_balance,
        transaction_details_dtos=mock_transaction_dtos
    )

    storage.get_wallet_balance.return_value = mock_wallet_balance
    storage.get_transaction_details_dtos.return_value = mock_transaction_dtos
    presenter.get_wallet_transaction_details_response.return_value = \
        mock_presenter_response

    #Act
    wallet_transactions_details = interactor.get_wallet_transactions_details(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert wallet_transactions_details == mock_presenter_response
    storage.get_wallet_balance.assert_called_once_with(user_id=user_id)
    storage.get_transaction_details_dtos.assert_called_once_with(
        user_id=user_id, limit=5, offset=0
    )
    presenter.get_wallet_transaction_details_response.assert_called_once_with(
        wallet_transactions_dto=expected_wallet_transactions_dto
    )
