import pytest
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation


@pytest.mark.django_db
def test_get_existing_item_ids_in_order_items_for_given_item_ids_returns_list_of_ids(
        users, forms, sections, items, ordered_items):
    #Arrange
    user_id = 1
    expected_item_ids_from_db = [1, 2]
    order_item_storage = OrderItemStorageImplementation()

    #Act
    item_ids_from_db = \
        order_item_storage.get_existing_item_ids_of_user_in_order_items(
            user_id=user_id
        )

    #Assert
    assert item_ids_from_db == expected_item_ids_from_db


@pytest.mark.django_db
def test_get_existing_item_ids_in_order_items_when_no_orders_returns_empty_list(
        users, forms, sections, items):
    #Arrange
    user_id = 1
    expected_item_ids_from_db = []
    order_item_storage = OrderItemStorageImplementation()

    #Act
    item_ids_from_db = \
        order_item_storage.get_existing_item_ids_of_user_in_order_items(
            user_id=user_id
        )

    #Assert
    assert item_ids_from_db == expected_item_ids_from_db
