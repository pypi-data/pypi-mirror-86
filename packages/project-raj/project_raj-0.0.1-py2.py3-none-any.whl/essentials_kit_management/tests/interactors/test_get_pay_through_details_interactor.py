from mock import create_autospec
from essentials_kit_management.interactors.\
    get_pay_through_details_interactor import GetPayThroughDetailsInteractor
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface


def test_get_pay_through_details_interactor_returns_upi_id():
    #Arrange
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetPayThroughDetailsInteractor(
        storage=storage, presenter=presenter
    )

    mock_upi_id = "8247088772@SBI"
    mock_presenter_response = {'upi_id': mock_upi_id}

    storage.get_upi_id.return_value = mock_upi_id
    presenter.get_pay_through_details_response.return_value = \
        mock_presenter_response

    #Act
    upi_id_response = interactor.get_pay_through_details()

    #Assert
    assert upi_id_response == mock_presenter_response
    storage.get_upi_id.assert_called_once()
    presenter.get_pay_through_details_response.assert_called_once_with(
        upi_id=mock_upi_id
    )
