import pytest
import datetime
from freezegun import freeze_time
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import OrderedItemDto
from essentials_kit_management.constants.enums import StatusEnum


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_ordered_items_of_form_returns_dtos_list(
        forms, ordered_items, brands, item_dtos):
    #Arrange
    user_id = 1
    order_item_storage = OrderItemStorageImplementation()
    expected_ordered_items_dtos = [
        OrderedItemDto(
            ordered_item_id=1, user_id=1, item_id=1,
            brand_id=2, form_id=1, item_price=100.0, ordered_quantity=10,
            delivered_quantity=7, is_out_of_stock=True
        ),
        OrderedItemDto(
            ordered_item_id=2, user_id=1, item_id=2, brand_id=1,
            form_id=1, item_price=200.0, ordered_quantity=7,
            delivered_quantity=7, is_out_of_stock=False
        )
    ]

    #Act
    ordered_items_dtos = \
        order_item_storage.get_user_ordered_item_dtos_of_form(
            item_dtos=item_dtos, user_id=user_id
        )

    #Assert
    assert ordered_items_dtos == expected_ordered_items_dtos


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_ordered_items_of_form_when_no_items_returns_empty_list(
        forms, ordered_items, brands):
    #Arrange
    user_id = 1
    item_dtos = []
    order_item_storage = OrderItemStorageImplementation()
    expected_ordered_items_dtos = []

    #Act
    ordered_items_dtos = \
        order_item_storage.get_user_ordered_item_dtos_of_form(
            item_dtos=item_dtos, user_id=user_id
        )

    #Assert
    assert ordered_items_dtos == expected_ordered_items_dtos
