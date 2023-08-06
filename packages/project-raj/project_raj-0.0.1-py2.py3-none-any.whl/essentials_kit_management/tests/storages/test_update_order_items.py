import pytest
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.models import OrderItem
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


@pytest.mark.django_db
def test_update_order_items_perform_update_order_items_in_db(
        users, items, brands):
    #Arrange
    user_id = 1
    item_ids = [1]
    expected_item_id = 1
    expected_updated_brand_id = 3
    expected_updated_ordered_quantity = 7
    expected_order_item_id = 1

    update_item_details_dtos = [
        PostItemDetailsDto(
            item_id=1, brand_id=3, ordered_quantity=7
        )
    ]
    order_storage = OrderItemStorageImplementation()

    OrderItem.objects.create(
        user_id=user_id, item_id=1, brand_id=1, ordered_quantity=5
    )

    #Act
    order_storage.update_order_items(
        user_id=user_id, item_details_dtos=update_item_details_dtos,
        item_ids=item_ids
    )

    #Assert
    order = OrderItem.objects.get(id=1)

    assert order.id == expected_order_item_id
    assert order.item_id == expected_item_id
    assert order.brand_id == expected_updated_brand_id
    assert order.ordered_quantity == expected_updated_ordered_quantity
