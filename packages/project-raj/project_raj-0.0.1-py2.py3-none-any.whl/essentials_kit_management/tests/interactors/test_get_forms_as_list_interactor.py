import pytest
from freezegun import freeze_time
from mock import create_autospec
import datetime
from essentials_kit_management.interactors.get_forms_interactor \
    import GetFormsInteractor
from essentials_kit_management.interactors.storages.dtos \
    import FormDto, FormsListMetricsDto, OrderedItemDto, \
    CompleteFormsDetailsDto
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface
from essentials_kit_management.constants.enums import StatusEnum


def test_get_forms_interactor_returns_forms_details_list(
        form_dtos, ordered_item_dtos, mock_forms_presenter_response):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = form_dtos
    mock_ordered_items_dtos = ordered_item_dtos
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_items_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count=total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_items_dtos
    )

    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=15, estimated_cost=4500.0,
            items_pending=3, cost_incurred=3900.0
        ),
        FormsListMetricsDto(
            form_id=2, items_count=0, estimated_cost=0,
            items_pending=0, cost_incurred=0
        ),
        FormsListMetricsDto(
            form_id=3, items_count=0, estimated_cost=0,
            items_pending=0, cost_incurred=0
        )
    ]

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


def test_get_forms_interactor_with_no_forms_returns_empty_dto():
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10
    
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = []
    mock_ordered_items_dtos = []
    mock_presenter_response = {}

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_items_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_items_dtos
    )
    expected_form_list_metrics_dtos = []

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


def test_get_forms_interactor_with_all_ordered_items_delivered_returns_pending_count_to_zero(
        form_dtos_with_one_form, mock_forms_presenter_response):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = form_dtos_with_one_form
    mock_ordered_item_dtos = [
        OrderedItemDto(
            user_id=1, item_id=1, ordered_item_id=1,
            brand_id=1, form_id=1, item_price=200.0,
            ordered_quantity=10, delivered_quantity=10,
            is_out_of_stock=True
        )
    ]
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_item_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_item_dtos
    )

    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=10, estimated_cost=2000.0,
            items_pending=0, cost_incurred=2000.0
        )
    ]
    expected_pending_count_of_form_one = 0

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    form_one = forms_details[0]
    assert form_one['items_pending'] == expected_pending_count_of_form_one
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


def test_get_forms_interactor_estimated_cost_for_items_considering_quantity_ordered(
        form_dtos_with_one_form, mock_forms_presenter_response,
        ordered_item_dtos):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = form_dtos_with_one_form
    mock_ordered_item_dtos = ordered_item_dtos
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_item_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_item_dtos
    )

    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=15, estimated_cost=4500.0,
            items_pending=3, cost_incurred=3900.0
        )
    ]

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


def test_get_forms_interactor_when_no_items_delivered_returns_cost_incurred_zero(
        form_dtos_with_one_form, mock_forms_presenter_response,
        ordered_item_dtos):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = form_dtos_with_one_form
    mock_ordered_item_dtos = [
        OrderedItemDto(
            user_id=1, item_id=1, ordered_item_id=1,
            brand_id=1, form_id=1, item_price=200.0,
            ordered_quantity=10, delivered_quantity=0,
            is_out_of_stock=True
        )
    ]
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_item_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_item_dtos
    )

    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=10, estimated_cost=2000.0,
            items_pending=10, cost_incurred=0.0
        )
    ]

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


@freeze_time("2020-05-17 20:22:46")
def test_get_forms_interactor_when_live_status_expires_changes_status_to_closed(
        mock_forms_presenter_response, ordered_item_dtos):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10
    
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details_dtos = [
        FormDto(
            form_id=1, form_name='SnacksForm',
            form_description='This is form',
            form_status=StatusEnum.LIVE.value,
            close_date=datetime.datetime(2020, 5, 17, 19, 22, 46),
            expected_delivery_date=None
        )
    ]
    mock_ordered_item_dtos = [
        OrderedItemDto(
            user_id=1, item_id=1, ordered_item_id=1,
            brand_id=1, form_id=1, item_price=200.0,
            ordered_quantity=10, delivered_quantity=0,
            is_out_of_stock=True
        )
    ]
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_item_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_item_dtos
    )
    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=10, estimated_cost=2000.0,
            items_pending=10, cost_incurred=0.0
        )
    ]

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )


@freeze_time("2020-05-17 20:22:46")
def test_get_forms_interactor_when_all_items_delivered_status_changes_done(
        mock_forms_presenter_response, ordered_item_dtos):
    #Arrange
    user_id = 1
    offset = 0
    limit = 5
    total_forms_count = 10

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )


    mock_form_details_dtos = [
        FormDto(
            form_id=1, form_name='SnacksForm',
            form_description='This is form',
            form_status=StatusEnum.LIVE.value,
            close_date=datetime.datetime(2020, 5, 17, 19, 22, 46),
            expected_delivery_date=None
        )
    ]
    mock_ordered_item_dtos = [
        OrderedItemDto(
            user_id=1, item_id=1, ordered_item_id=1,
            brand_id=1, form_id=1, item_price=200.0,
            ordered_quantity=10, delivered_quantity=10,
            is_out_of_stock=True
        )
    ]
    mock_presenter_response = mock_forms_presenter_response

    form_storage.get_forms_details_as_list.return_value = \
        mock_form_details_dtos
    form_storage.get_total_forms_count.return_value = total_forms_count
    order_item_storage.get_ordered_items_dtos_of_user.return_value = \
        mock_ordered_item_dtos
    presenter.get_forms_details_response.return_value = \
        mock_presenter_response

    expected_forms_details = CompleteFormsDetailsDto(
        total_forms_count = total_forms_count,
        form_dtos=mock_form_details_dtos,
        ordered_item_dtos=mock_ordered_item_dtos
    )
    expected_form_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=10, estimated_cost=2000.0,
            items_pending=0, cost_incurred=2000.00
        )
    ]

    #Act
    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    #Assert
    assert forms_details == mock_presenter_response
    form_storage.get_forms_details_as_list.assert_called_once_with(
        offset=offset, limit=limit
    )
    order_item_storage.get_ordered_items_dtos_of_user.assert_called_once_with(
        user_id=user_id
    )
    presenter.get_forms_details_response.assert_called_once_with(
        forms_details=expected_forms_details,
        forms_list_metrics_dtos=expected_form_list_metrics_dtos
    )
