import pytest
from mock import create_autospec
from django_swagger_utils.drf_server.exceptions import NotFound
from essentials_kit_management.interactors.\
    get_order_details_of_form_interactor import \
    GetOrderDetailsOfFormInteractor
from essentials_kit_management.interactors.storages.dtos \
    import OrderedFormMetricsDto, ItemMetricsDto, FormsListMetricsDto, \
    OrderDetailsOfFormDto
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface


def test_get_order_details_of_form_interactor_with_invalid_form_id_raises_exception():
    #Arrange
    invalid_form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetOrderDetailsOfFormInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    form_storage.validate_form_id.return_value = False
    presenter.raise_invalid_form_exception.side_effect = NotFound

    #Act
    with pytest.raises(NotFound):
        interactor.get_order_details_of_form(
            form_id=invalid_form_id, user_id=user_id
        )

    #Assert
    form_storage.validate_form_id.assert_called_once_with(
        form_id=invalid_form_id
    )
    presenter.raise_invalid_form_exception.assert_called_once()


def test_get_order_details_of_form_interactor_with_valid_form_id_returns_dto(
        section_dtos, item_dtos, brand_dtos, user_ordered_item_details_dtos,
        get_oder_details_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetOrderDetailsOfFormInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_ordered_item_dtos = user_ordered_item_details_dtos
    mock_presenter_response = get_oder_details_presenter_response

    expected_item_metrics_dtos = [
        ItemMetricsDto(
            item_id=1, item_name='item 1', quantity_added_for_item=10,
            cost_incurred_for_item=1400.0, quantity_received_for_item=7,
            is_out_of_stock=True
        ),
        ItemMetricsDto(
            item_id=2, item_name='item 1',
            quantity_added_for_item=5, cost_incurred_for_item=2500.0,
            quantity_received_for_item=5, is_out_of_stock=False
        )
    ]
    expected_form_metrics_dto = OrderedFormMetricsDto(
        total_items_count=15, total_cost_incurred=3900.0,
        total_received_items_count=12
    )
    expected_ordered_details_of_form_dto = OrderDetailsOfFormDto(
        form_id=form_id,
        item_metrics_dtos=expected_item_metrics_dtos,
        form_metrics_dto=expected_form_metrics_dto
    )

    form_storage.validate_form_id.return_value = True
    order_item_storage.get_user_ordered_details_dtos_of_form.return_value = \
        mock_ordered_item_dtos
    presenter.get_order_details_of_form_response.return_value = \
        mock_presenter_response

    #Act
    ordered_details_of_form = interactor.get_order_details_of_form(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert ordered_details_of_form == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    order_item_storage.get_user_ordered_details_dtos_of_form.\
        assert_called_once_with(form_id=form_id, user_id=user_id)
    presenter.get_order_details_of_form_response.assert_called_once_with(
        ordered_details_of_form_dto=expected_ordered_details_of_form_dto
    )


def test_get_order_details_of_form_interactor_with_no_orders_returns_empty_item_metrics_dtos(
        section_dtos, item_dtos, brand_dtos,
        get_oder_details_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetOrderDetailsOfFormInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_ordered_item_dtos = []
    mock_presenter_response = get_oder_details_presenter_response

    expected_item_metrics_dtos = []
    expected_form_metrics_dto = OrderedFormMetricsDto(
        total_items_count=0, total_cost_incurred=0,
        total_received_items_count=0
    )
    expected_ordered_details_of_form_dto = OrderDetailsOfFormDto(
        form_id=form_id,
        item_metrics_dtos=expected_item_metrics_dtos,
        form_metrics_dto=expected_form_metrics_dto
    )

    form_storage.validate_form_id.return_value = True
    order_item_storage.get_user_ordered_details_dtos_of_form.return_value = \
        mock_ordered_item_dtos
    presenter.get_order_details_of_form_response.return_value = \
        mock_presenter_response

    #Act
    ordered_details_of_form = interactor.get_order_details_of_form(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert ordered_details_of_form == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    order_item_storage.get_user_ordered_details_dtos_of_form.\
        assert_called_once_with(form_id=form_id, user_id=user_id)
    presenter.get_order_details_of_form_response.assert_called_once_with(
        ordered_details_of_form_dto=expected_ordered_details_of_form_dto
    )
