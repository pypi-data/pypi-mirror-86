import datetime
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.storages.dtos \
    import FormDto, CompleteFormsDetailsDto, \
    OrderedItemDto, FormsListMetricsDto
from essentials_kit_management.constants.enums import StatusEnum


def test_get_forms_details_response_returns_list_of_dicts():
    #Assert
    total_forms_count = 10

    json_presenter = PresenterImplementation()
    form_details_dto = CompleteFormsDetailsDto(
        total_forms_count=total_forms_count,
        form_dtos=[
            FormDto(
                form_id=1, form_name='SnacksForm',
                form_description='This is form',
                form_status=StatusEnum.LIVE.value, close_date=None,
                expected_delivery_date='2020-05-17 20:22:46'
            ),
            FormDto(
                form_id=2, form_name='SnksForm',
                form_description='This is form',
                form_status=StatusEnum.CLOSED.value, close_date=None,
                expected_delivery_date='2020-05-17 20:22:46'
            ),
            FormDto(
                form_id=3, form_name='SForm', form_description='This is form',
                form_status=StatusEnum.LIVE.value, close_date=None,
                expected_delivery_date='2020-05-17 20:22:46'
            )
        ],
        ordered_item_dtos=[
            OrderedItemDto(
                user_id=1, item_id=1, ordered_item_id=1,
                brand_id=1, form_id=1, item_price=200.0,
                ordered_quantity=10, delivered_quantity=7,
                is_out_of_stock=True),
            OrderedItemDto(
                user_id=1, item_id=2, ordered_item_id=2, brand_id=2,
                form_id=1, item_price=500.0, ordered_quantity=5,
                delivered_quantity=6, is_out_of_stock=False
            )
        ]
    )

    forms_list_metrics_dtos = [
        FormsListMetricsDto(
            form_id=1, items_count=2, estimated_cost=4500.0,
            items_pending=1, cost_incurred=3900.0
        ),
        FormsListMetricsDto(
            form_id=2, items_count=0, estimated_cost=0,
            items_pending=0, cost_incurred=0
        ),
        FormsListMetricsDto(
            form_id=3, items_count=0, estimated_cost=0,
            items_pending=0, cost_incurred=0
        )
    ]

    expected_output = {
        'forms': [
            {
                'close_date': None,
                'cost_incurred': 3900.0,
                'estimated_cost': 4500.0,
                'expected_delivery_date': '2020-05-17 20:22:46',
                'form_description': 'This is form',
                'form_id': 1,
                'form_name': 'SnacksForm',
                'form_status': 'LIVE',
                'items_count': 2,
                'items_pending': 1
            },
            {
                'close_date': None,
                'cost_incurred': 0,
                'estimated_cost': 0,
                'expected_delivery_date': '2020-05-17 20:22:46',
                'form_description': 'This is form',
                'form_id': 2,
                'form_name': 'SnksForm',
                'form_status': 'CLOSED',
                'items_count': 0,
                'items_pending': 0
            },
            {
                'close_date': None,
                'cost_incurred': 0,
                'estimated_cost': 0,
                'expected_delivery_date': '2020-05-17 20:22:46',
                'form_description': 'This is form',
                'form_id': 3,
                'form_name': 'SForm',
                'form_status': 'LIVE',
                'items_count': 0,
                'items_pending': 0
            }
        ],
    'forms_count': 10
    }

    #Act
    output = json_presenter.get_forms_details_response(
        form_details_dto, forms_list_metrics_dtos
    )

    #Assert
    assert output == expected_output
