import datetime
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.storages.dtos \
    import ItemMetricsDto, OrderedFormMetricsDto, OrderedFormMetricsDto, \
    OrderDetailsOfFormDto


def test_get_order_details_of_form_response_returns_dict():
    #Assert
    form_id = 1
    json_presenter = PresenterImplementation()
    item_metrics_dtos = [
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
    form_metrics_dto = OrderedFormMetricsDto(
        total_items_count=15, total_cost_incurred=3900.0,
        total_received_items_count=12
    )
    ordered_details_of_form_dto = OrderDetailsOfFormDto(
        form_id=form_id,
        item_metrics_dtos=item_metrics_dtos,
        form_metrics_dto=form_metrics_dto
    )

    expected_output = {
        'form_id': 1,
        'order_details': [
            {
                'cost_incurred_for_item': 1400.0,
                'is_out_of_stock': True,
                'item_id': 1,
                'item_name': 'item 1',
                'quantity_added_for_item': 10,
                'quantity_received_for_item': 7
            },
            {
                'cost_incurred_for_item': 2500.0,
                'is_out_of_stock': False,
                'item_id': 2,
                'item_name': 'item 1',
                'quantity_added_for_item': 5,
                'quantity_received_for_item': 5
            }
        ],
        'total_cost_incurred': 3900.0,
        'total_items_count': 15,
        'total_received_items_count': 12
    }

    #Act
    output = json_presenter.get_order_details_of_form_response(
        ordered_details_of_form_dto=ordered_details_of_form_dto
    )

    #Assert
    assert output == expected_output
