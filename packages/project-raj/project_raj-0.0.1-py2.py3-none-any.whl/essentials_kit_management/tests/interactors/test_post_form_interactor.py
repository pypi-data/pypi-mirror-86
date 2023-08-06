import pytest
from mock import create_autospec
from django_swagger_utils.drf_server.exceptions import NotFound
from essentials_kit_management.interactors.post_form_interactor \
    import PostFormInteractor
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface

def test_post_form_interactor_with_invalid_form_id_raises_exception(
        get_item_details_list):
    #Arrange
    user_id = 1
    invalid_form_id = 1
    item_details_list = get_item_details_list

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        storage=storage, presenter=presenter
    )

    form_storage.validate_form_id.return_value = False
    presenter.raise_invalid_form_exception.side_effect = NotFound

    #Act
    with pytest.raises(NotFound):
        interactor.post_form_details(
            user_id=user_id, form_id = invalid_form_id,
            item_details_list=item_details_list
        )

    #Assert
    form_storage.validate_form_id.assert_called_once_with(
        form_id=invalid_form_id
    )
    presenter.raise_invalid_form_exception.assert_called_once()


def test_post_form_interactor_with_invalid_item_id_raises_exception(
        get_item_details_list):
    #Arrange
    user_id = 1
    form_id = 1
    invalid_item_ids = [1]
    item_details_list = get_item_details_list

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        storage=storage, presenter=presenter
    )
    mock_item_ids_from_db = []

    storage.get_item_ids_from_db_if_given_ids_valid.return_value = \
        mock_item_ids_from_db
    presenter.raise_invalid_item_id_exception.side_effect = NotFound

    #Act
    with pytest.raises(NotFound):
        interactor.post_form_details(
            user_id=user_id, form_id = form_id,
            item_details_list=item_details_list
        )

    #Assert
    storage.get_item_ids_from_db_if_given_ids_valid.assert_called_once_with(
        item_ids=invalid_item_ids)
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    presenter.raise_invalid_item_id_exception.assert_called_once()


def test_post_form_interactor_with_invalid_brand_id_raises_exception(
        get_item_details_list):
    #Arrange
    user_id = 1
    form_id = 1
    item_ids = [1]
    invalid_brand_ids = [1]
    item_details_list = get_item_details_list

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        storage=storage, presenter=presenter
    )

    mock_item_ids_from_db = [1]
    mock_brand_ids_from_db = []

    storage.get_item_ids_from_db_if_given_ids_valid.return_value = \
        mock_item_ids_from_db
    storage.get_brand_ids_from_db_if_given_ids_valid.return_value = \
        mock_brand_ids_from_db
    presenter.raise_invalid_brand_id_exception.side_effect = NotFound

    #Act
    with pytest.raises(NotFound):
        interactor.post_form_details(
            user_id=user_id, form_id = form_id,
            item_details_list=item_details_list
        )

    #Assert
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    storage.get_item_ids_from_db_if_given_ids_valid.assert_called_once_with(
        item_ids=item_ids)
    storage.get_brand_ids_from_db_if_given_ids_valid.assert_called_once_with(
        brand_ids=invalid_brand_ids)
    presenter.raise_invalid_brand_id_exception.assert_called_once()


def test_post_form_interactor_creates_orders_for_given_items(
        get_item_details_list, get_post_item_details_dto):
    #Arrange
    user_id = 1
    form_id = 1
    item_details_dtos = get_post_item_details_dto
    item_details_list = get_item_details_list

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        storage=storage, presenter=presenter
    )

    mock_item_ids = [1]
    mock_brand_ids = [1]
    mock_item_ids_to_delete_orders = []
    order_item_storage.\
        get_existing_item_ids_of_user_in_order_items.return_value = []
    storage.get_item_ids_from_db_if_given_ids_valid.return_value = \
        mock_item_ids
    storage.get_brand_ids_from_db_if_given_ids_valid.return_value = \
        mock_brand_ids

    #Act
    interactor.post_form_details(
        user_id=user_id, form_id=form_id, item_details_list=item_details_list
    )

    #Assert
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    storage.get_item_ids_from_db_if_given_ids_valid.assert_called_once_with(
        item_ids=mock_item_ids
    )
    storage.get_brand_ids_from_db_if_given_ids_valid.assert_called_once_with(
        brand_ids=mock_brand_ids
    )
    order_item_storage.get_existing_item_ids_of_user_in_order_items.\
        assert_called_once_with(user_id=user_id)
    order_item_storage.delete_orders_of_user_for_given_item_ids.\
        assert_called_once_with(
            item_ids_to_delete_orders=mock_item_ids_to_delete_orders,
            user_id=user_id, form_id=form_id
        )
    order_item_storage.create_order_items.assert_called_once_with(
        user_id=user_id, form_id=form_id, item_details_dtos=item_details_dtos
    )
    presenter.post_form_details_response.assert_called()


def test_post_form_interactor_with_update_order_updates_existing_order(
        get_item_details_list, get_post_item_details_dto):
    #Arrange
    user_id = 1
    form_id = 1
    item_details_dtos = get_post_item_details_dto
    item_details_list = get_item_details_list

    form_storage = create_autospec(FormStorageInterface)
    order_item_storage = create_autospec(OrderItemStorageInterface)
    storage = create_autospec(StorageInterface)
    presenter = create_autospec(PresenterInterface)
    interactor = PostFormInteractor(
        form_storage=form_storage, order_item_storage=order_item_storage,
        storage=storage, presenter=presenter
    )

    mock_existing_orders_ids = [1]
    mock_item_ids = [1]
    mock_brand_ids = [1]
    mock_item_ids_to_delete_orders = []
    order_item_storage.get_existing_item_ids_of_user_in_order_items.\
        return_value = mock_existing_orders_ids
    storage.get_item_ids_from_db_if_given_ids_valid.return_value = \
        mock_item_ids
    storage.get_brand_ids_from_db_if_given_ids_valid.return_value = \
        mock_brand_ids

    #Act
    interactor.post_form_details(
        user_id=user_id, form_id=form_id, item_details_list=item_details_list
    )

    #Assert
    form_storage.validate_form_id.assert_called_once_with(form_id=form_id)
    storage.get_item_ids_from_db_if_given_ids_valid.assert_called_once_with(
        item_ids=mock_item_ids
    )
    storage.get_brand_ids_from_db_if_given_ids_valid.assert_called_once_with(
        brand_ids=mock_brand_ids
    )
    order_item_storage.get_existing_item_ids_of_user_in_order_items.\
        assert_called_once_with(user_id=user_id)
    order_item_storage.delete_orders_of_user_for_given_item_ids.\
        assert_called_once_with(
            item_ids_to_delete_orders=mock_item_ids_to_delete_orders,
            user_id=user_id, form_id=form_id
        )
    order_item_storage.update_order_items.assert_called_once_with(
        user_id=user_id, item_ids=mock_existing_orders_ids,
        item_details_dtos=item_details_dtos
    )
    presenter.post_form_details_response.assert_called()
