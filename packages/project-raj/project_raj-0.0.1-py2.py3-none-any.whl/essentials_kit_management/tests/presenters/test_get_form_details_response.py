import datetime
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.storages.dtos \
    import FormDetailsDto, SectionDto, ItemDto, \
    BrandDto, CompleteFormDetailsDto, FormMetricsDto
from essentials_kit_management.constants.enums import StatusEnum


def test_get_form_details_response_returns_dict():
    #Assert
    json_presenter = PresenterImplementation()
    complete_form_details_dto = CompleteFormDetailsDto(
        FormDetailsDto(
            form_id=3, form_description='This is fruits form',
            form_name='Snacks Form', close_date='2020-05-09 08:11:12',
            section_dtos=[
                SectionDto(
                    section_id=5, form_id=3, product_title='fruits',
                    product_description='FruitsSec'
                )
            ],
            item_dtos=[
                ItemDto(
                    item_id=9, section_id=5, item_name='Mango',
                    item_description='fruit'
                ),
                ItemDto(
                    item_id=10, section_id=5, item_name='Papaya',
                    item_description='fruit'
                )
            ],
            brand_dtos=[
                BrandDto(
                    item_id=11, brand_id=19, brand_name='XXXX',
                    item_price=200.0, min_quantity=10, max_quantity=20
                )
            ]
        ),
        ordered_item_dtos = []
    )

    form_metrics_dto = FormMetricsDto(total_cost=400.0, total_items=10)

    expected_output = {
        'form_id': 3,
        'form_name': 'Snacks Form',
        'form_description': 'This is fruits form',
        'close_date': '2020-05-09 08:11:12',
        'sections': [
            {
                'section_id': 5,
                'section_name': 'fruits',
                'section_description': 'FruitsSec',
                'item_details': [
                    {
                        'item_id': 9,
                        'item_name': 'Mango',
                        'item_description': 'fruit',
                        'item_brands': [],
                        'order_details': None
                    },
                    {
                        'item_id': 10,
                        'item_name': 'Papaya',
                        'item_description': 'fruit',
                        'item_brands': [],
                        'order_details': None
                    }
                ]
            }
        ],
        'total_cost': 400.0,
        'total_items': 10
    }

    #Act
    output = json_presenter.get_form_details_response(
        complete_form_details_dto, form_metrics_dto
    )

    #Assert
    assert output == expected_output
