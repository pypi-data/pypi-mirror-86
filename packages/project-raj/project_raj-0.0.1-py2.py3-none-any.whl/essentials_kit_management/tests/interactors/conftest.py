import pytest
import datetime
from essentials_kit_management.constants.enums import StatusEnum
from essentials_kit_management.interactors.storages.dtos \
    import SectionDto, FormDetailsDto, ItemDto, \
    BrandDto, OrderedItemDto, FormDto, UserOrderDetailsDto
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


@pytest.fixture()
def section_dtos():
    section_dtos=[
        SectionDto(
            section_id=1, form_id=1, product_title='Snacks',
            product_description='SnacksSec'
        ),
        SectionDto(
            section_id=2, form_id=1, product_title='Bikes',
            product_description='BikesSec'
        )
    ]
    return section_dtos


@pytest.fixture()
def item_dtos():
    item_dtos=[
        ItemDto(
            item_id=1, section_id=1, item_name='Cadbury',
            item_description='chocolate'
        ),
        ItemDto(
            item_id=2, section_id=2, item_name='Milk',
            item_description='Milk'
        )
    ]
    return item_dtos


@pytest.fixture()
def form_dtos_with_one_form():
    form_dto = [
        FormDto(
            form_id=1, form_name='SnacksForm',
            form_description='This is form',
            form_status=StatusEnum.LIVE.value, close_date=None,
            expected_delivery_date=datetime.datetime(2020, 5, 17, 20, 22, 46)
        )
    ]
    return form_dto


@pytest.fixture()
def form_dtos():
    form_dtos = [
        FormDto(
            form_id=1, form_name='SnacksForm',
            form_description='This is form',
            form_status=StatusEnum.LIVE.value, close_date=None,
            expected_delivery_date=datetime.datetime(2020, 5, 17, 20, 22, 46)
        ),
        FormDto(
            form_id=2, form_name='SnksForm',
            form_description='This is form',
            form_status=StatusEnum.CLOSED.value, close_date=None,
            expected_delivery_date=datetime.datetime(2020, 5, 17, 20, 22, 46)
        ),
        FormDto(
            form_id=3, form_name='SForm', form_description='This is form',
            form_status=StatusEnum.LIVE.value, close_date=None,
            expected_delivery_date=datetime.datetime(2020, 5, 17, 20, 22, 46)
        )
    ]
    return form_dtos


@pytest.fixture()
def brand_dtos():
    brand_dtos = [
        BrandDto(
            item_id=1, brand_id=1, brand_name='Adidas', item_price=200.0,
            min_quantity=10, max_quantity=20
        ),
        BrandDto(
            item_id=1, brand_id=2, brand_name='Puma',
            item_price=500.0, min_quantity=5, max_quantity=0
        ),
        BrandDto(
            item_id=2, brand_id=3, brand_name='Samsung',
            item_price=100.0, min_quantity=2, max_quantity=20
        ),
        BrandDto(
            item_id=2, brand_id=4, brand_name='Adidas',
            item_price=200.0, min_quantity=10, max_quantity=20
        )
    ]
    return brand_dtos


@pytest.fixture()
def ordered_item_dtos():
    ordered_item_dtos = [
        OrderedItemDto(
            user_id=1, item_id=1, ordered_item_id=1,
            brand_id=1, form_id=1, item_price=200.0,
            ordered_quantity=10, delivered_quantity=7,
            is_out_of_stock=True
        ),
        OrderedItemDto(
            user_id=1, item_id=2, ordered_item_id=2, brand_id=2,
            form_id=1, item_price=500.0, ordered_quantity=5,
            delivered_quantity=5, is_out_of_stock=False
        )
    ]
    return ordered_item_dtos


@pytest.fixture()
def form_mock_presenter_response():
    mock_presenter_response = {
        "description": "string",
        "section": [
            {
                "product_title": "string",
                "product_description": "string",
                "question": [
                    {
                        "item_name": "string",
                        "item_description": "string",
                        "item_brand": [
                            {
                                "brand_name": "string",
                                "item_price": 0,
                                "min_quantity": 0,
                                "max_quantity": 0
                            }
                        ]
                    }
                ]
            }
        ],
        "total_cost": 4500.0,
        "total_items": 15
    }

    return mock_presenter_response


@pytest.fixture()
def mock_forms_presenter_response():
    mock_presenter_response = [
        {
            "form_name": "Snacks",
            "form_status": "LIVE",
            "closed_date": "2020-05-27",
            "expected_delivery_date": "2020-05-27",
            "items_count": 0,
            "estimated_cost": 0,
            "items_pending": 0,
            "cost_incurred": 0
        }
    ]
    return mock_presenter_response


@pytest.fixture()
def get_item_details_list():
    item_details_list = [
        {
            "item_id": 1,
            "brand_details": {
                "brand_id": 1
          },
          "ordered_quantity": 8
        }
    ]
    return item_details_list


@pytest.fixture()
def get_post_item_details_dto():
    post_item_details_dto = [
        PostItemDetailsDto(
            item_id=1, brand_id=1, ordered_quantity=8
        )
    ]
    return post_item_details_dto


@pytest.fixture()
def get_oder_details_presenter_response():
    order_details_presenter_response = {
        "form_id": 1,
        "order_details": [
            {
                "item_id": 1,
                "item_name": "string",
                "quantity_added_for_item": 9,
                "cost_incurred_for_item": 9,
                "quantity_received_for_item": 1500.0,
                "is_out_of_stock": True
            }
        ],
        "total_items_count": 10,
        "total_cost_incurred": 2000.0,
        "total_received_items_count": 10
    }
    return order_details_presenter_response


@pytest.fixture()
def user_ordered_item_details_dtos():
    user_ordered_item_details_dtos = [
        UserOrderDetailsDto(
            item_id=1, item_name='item 1', ordered_item_id=1,
            item_price=200.0, ordered_quantity=10,
            delivered_quantity=7, is_out_of_stock=True
        ),
        UserOrderDetailsDto(
            item_id=2, item_name='item 1', ordered_item_id=2,
            item_price=500.0, ordered_quantity=5,
            delivered_quantity=5, is_out_of_stock=False
        )
    ]
    return user_ordered_item_details_dtos