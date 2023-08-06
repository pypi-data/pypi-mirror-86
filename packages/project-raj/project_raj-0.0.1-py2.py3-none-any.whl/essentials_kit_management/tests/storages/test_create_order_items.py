import pytest
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.models import OrderItem


@pytest.mark.django_db
def test_create_order_items_perform_save_orders_items_in_db(
        users, forms, items, brands, get_item_details_dtos):
    #Arrange
    user_id = 1
    form_id = 1
    expected_item_id_one = 1
    expected_brand_id_one = 1
    expected_ordered_quantity_one = 5
    expected_item_id_two = 2
    expected_brand_id_two = 3
    expected_ordered_quantity_two = 7
    expected_first_order_item_id = 1
    expected_second_order_item_id = 2

    item_details_dtos = get_item_details_dtos
    order_item_storage = OrderItemStorageImplementation()

    #Act
    order_item_storage.create_order_items(
        user_id=user_id, form_id=form_id, item_details_dtos=item_details_dtos
    )

    #Assert
    orders = OrderItem.objects.all()
    order_1 = orders[0]
    order_2 = orders[1]

    assert order_1.id == expected_first_order_item_id
    assert order_2.id == expected_second_order_item_id
    assert order_1.item_id == expected_item_id_one
    assert order_2.item_id == expected_item_id_two
    assert order_1.brand_id == expected_brand_id_one
    assert order_2.brand_id == expected_brand_id_two
    assert order_1.ordered_quantity == expected_ordered_quantity_one
    assert order_2.ordered_quantity == expected_ordered_quantity_two
