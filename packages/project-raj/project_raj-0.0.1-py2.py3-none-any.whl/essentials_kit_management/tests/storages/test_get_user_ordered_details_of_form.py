import pytest
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import UserOrderDetailsDto


@pytest.mark.django_db
def test_get_user_ordered_details_dtos_of_form_returns_dtos(
        forms, ordered_items, brands, items, sections):
    #Arrange
    form_id = 1
    user_id = 1
    order_item_storage = OrderItemStorageImplementation()

    expected_user_ordered_item_dtos = [
        UserOrderDetailsDto(
            ordered_item_id=1, item_id=1, item_name='Navaratna',
            item_price=100.0, ordered_quantity=10,
            delivered_quantity=7, is_out_of_stock=True
        ),
        UserOrderDetailsDto(
            ordered_item_id=2, item_id=2, item_name='Moong Dal',
            item_price=200.0, ordered_quantity=7,
            delivered_quantity=7, is_out_of_stock=False
        )
    ]

    #Act
    user_ordered_items_dtos = \
        order_item_storage.get_user_ordered_details_dtos_of_form(
            form_id=form_id, user_id=user_id
        )

    #Assert
    assert user_ordered_items_dtos == expected_user_ordered_item_dtos


@pytest.mark.django_db
def test_get_user_ordered_details_dtos_of_form_when_no_orders_returns_empty_list(
        forms, brands, items, sections):
    #Arrange
    form_id = 1
    user_id = 1
    order_item_storage = OrderItemStorageImplementation()

    expected_user_ordered_item_dtos = []

    #Act
    user_ordered_items_dtos = \
        order_item_storage.get_user_ordered_details_dtos_of_form(
            form_id=form_id, user_id=user_id
        )

    #Assert
    assert user_ordered_items_dtos == expected_user_ordered_item_dtos
