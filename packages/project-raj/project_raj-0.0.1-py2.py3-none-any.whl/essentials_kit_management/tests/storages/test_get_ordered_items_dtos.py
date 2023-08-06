import pytest
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import OrderedItemDto


@pytest.mark.django_db
def test_get_ordered_items_dtos_returns_list_of_dtos(ordered_items, users):
    #Arrange
    user_id = 1
    order_item_storage = OrderItemStorageImplementation()
    expected_ordered_items_dtos = [
        OrderedItemDto(
            ordered_item_id=1, user_id=1, item_id=1, brand_id=2,
            form_id=1, item_price=100.0, ordered_quantity=10,
            delivered_quantity=7, is_out_of_stock=True
        ),
        OrderedItemDto(
            ordered_item_id=2, user_id=1, item_id=2, brand_id=1,
            form_id=1, item_price=200.0, ordered_quantity=7,
            delivered_quantity=7, is_out_of_stock=False
        )
    ]

    #Act
    ordered_items_dtos = order_item_storage.get_ordered_items_dtos_of_user(
        user_id=user_id
    )

    #Assert
    assert ordered_items_dtos == expected_ordered_items_dtos


@pytest.mark.django_db
def test_get_ordered_items_dtos_when_no_orders_returns_empty_list():
    #Arrange
    user_id = 1
    order_item_storage = OrderItemStorageImplementation()
    expected_ordered_items_dtos = []

    #Act
    ordered_items_dtos = order_item_storage.get_ordered_items_dtos_of_user(
        user_id=user_id
    )

    #Assert
    assert ordered_items_dtos == expected_ordered_items_dtos
