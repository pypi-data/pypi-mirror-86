import pytest
from mock import create_autospec
from django_swagger_utils.drf_server.exceptions import NotFound
from essentials_kit_management.interactors.get_form_interactor \
    import GetFormInteractor
from essentials_kit_management.interactors.storages.dtos \
    import FormMetricsDto, FormDetailsDto, CompleteFormDetailsDto
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface


def test_get_form_interactor_with_valid_form_id_returns_forms_details(
        section_dtos, item_dtos, brand_dtos,
        ordered_item_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=section_dtos,
        item_dtos=item_dtos,
        brand_dtos=brand_dtos
    )
    mock_ordered_items = ordered_item_dtos
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=4500.0, total_items=15)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )


def test_get_form_interactor_when_no_sections_returns_empty_section_list(
        item_dtos, brand_dtos,
        ordered_item_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=[],
        item_dtos=item_dtos,
        brand_dtos=brand_dtos
    )
    mock_ordered_items = ordered_item_dtos
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=4500.0, total_items=15)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )


def test_get_form_interactor_when_no_items_returns_empty_items_list(
        section_dtos, brand_dtos,
        ordered_item_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    item_dtos = []
    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=section_dtos,
        item_dtos=item_dtos,
        brand_dtos=brand_dtos
    )
    mock_ordered_items = ordered_item_dtos
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=4500.0, total_items=15)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )


def test_get_form_interactor_when_no_brands_returns_empty_brands_list(
        item_dtos, section_dtos,
        ordered_item_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=section_dtos,
        item_dtos=item_dtos,
        brand_dtos=[]
    )
    mock_ordered_items = ordered_item_dtos
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=4500.0, total_items=15)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )


def test_get_form_interactor_when_no_ordered_items_returns_empty_ordered_items_list(
        item_dtos, section_dtos,
        brand_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=section_dtos,
        item_dtos=item_dtos,
        brand_dtos=brand_dtos
    )
    mock_ordered_items = []
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=0.0, total_items=0)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )


def test_get_form_interactor_when_no_ordered_items_returns_metrics_values_zero(
        item_dtos, section_dtos,
        brand_dtos, form_mock_presenter_response):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = GetFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        presenter=presenter
    )

    mock_form_details = FormDetailsDto(
        form_id=1,
        form_name='SnacksForm',
        form_description='This is form',
        close_date='2020-05-17 20:22:46',
        section_dtos=section_dtos,
        item_dtos=item_dtos,
        brand_dtos=brand_dtos
    )
    mock_ordered_items = []
    mock_presenter_response = form_mock_presenter_response

    complete_form_details_dto = CompleteFormDetailsDto(
        form_details_dto=mock_form_details,
        ordered_item_dtos=mock_ordered_items
    )

    expected_form_metrics_dto = \
        FormMetricsDto(total_cost=0.0, total_items=0)

    form_storage.validate_form_id.return_value = True
    form_storage.get_form_details_dto.return_value = mock_form_details
    order_item_storage.get_user_ordered_item_dtos_of_form.return_value = \
        mock_ordered_items
    presenter.get_form_details_response.return_value = mock_presenter_response

    #Act
    form_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details == mock_presenter_response
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    form_storage.get_form_details_dto.assert_called_once_with(
        form_id=form_id, user_id=user_id
    )
    order_item_storage.get_user_ordered_item_dtos_of_form.\
        assert_called_once_with(item_dtos=item_dtos, user_id=user_id)
    presenter.get_form_details_response.assert_called_once_with(
        complete_form_details_dto=complete_form_details_dto,
        form_metrics_dto=expected_form_metrics_dto
    )
