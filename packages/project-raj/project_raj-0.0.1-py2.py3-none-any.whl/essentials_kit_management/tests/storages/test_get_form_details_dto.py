import pytest
import datetime
from freezegun import freeze_time
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import FormDetailsDto, SectionDto, ItemDto, BrandDto


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_form_details_returns_dto(forms, sections, items, brands):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = FormStorageImplementation()
    expected_form_details_dto = FormDetailsDto(
        form_id=1, form_description='This is snacks form',
        form_name='Snacks Form',
        close_date=datetime.datetime(2020, 6, 7, 5, 4, 3),
        section_dtos=[
            SectionDto(
                section_id=1, form_id=1, product_title='Snack Items',
                product_description='SnacksSec'
            ),
            SectionDto(
                section_id=2, form_id=1, product_title='Biscuits',
                product_description='BiscuitsSec'
            )
        ],
        item_dtos=[
            ItemDto(
                item_id=1, section_id=1, item_name='Navaratna',
                item_description='50 mg'
            ),
            ItemDto(
                item_id=2, section_id=1, item_name='Moong Dal',
                item_description='100 mg'
            )
        ],
        brand_dtos=[
            BrandDto(
                item_id=1, brand_id=1, brand_name='XXXX', item_price=200.0,
                min_quantity=10, max_quantity=20
            ),
            BrandDto(
                item_id=1, brand_id=2, brand_name='YYYY', item_price=100.0,
                min_quantity=5, max_quantity=10
            ),
            BrandDto(
                item_id=1, brand_id=3, brand_name='ZZZZ',
                item_price=100.0, min_quantity=2, max_quantity=20
            )
        ]
    )

    #Act
    form_details_dto = form_storage.get_form_details_dto(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details_dto == expected_form_details_dto


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_forms_details_dto_when_no_brands_exists_returns_empty_list_of_brands(
        forms, sections, items):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = FormStorageImplementation()
    expected_form_details_dto = FormDetailsDto(
        form_id=1, form_description='This is snacks form',
        form_name='Snacks Form',
        close_date=datetime.datetime(2020, 6, 7, 5, 4, 3),
        section_dtos=[
            SectionDto(
                section_id=1, form_id=1, product_title='Snack Items',
                product_description='SnacksSec'
            ),
            SectionDto(
                section_id=2, form_id=1, product_title='Biscuits',
                product_description='BiscuitsSec'
            )
        ],
        item_dtos=[
            ItemDto(
                item_id=1, section_id=1, item_name='Navaratna',
                item_description='50 mg'
            ),
            ItemDto(
                item_id=2, section_id=1, item_name='Moong Dal',
                item_description='100 mg'
            )
        ],
        brand_dtos=[]
    )

    #Act
    form_details_dto = form_storage.get_form_details_dto(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details_dto == expected_form_details_dto


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_forms_details_dto_when_no_items_exists_returns_empty_list_of_items_and_brands(
        forms, sections):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = FormStorageImplementation()
    expected_form_details_dto = FormDetailsDto(
        form_id=1, form_description='This is snacks form',
        form_name='Snacks Form',
        close_date=datetime.datetime(2020, 6, 7, 5, 4, 3),
        section_dtos=[
            SectionDto(
                section_id=1, form_id=1, product_title='Snack Items',
                product_description='SnacksSec'
            ),
            SectionDto(
                section_id=2, form_id=1, product_title='Biscuits',
                product_description='BiscuitsSec'
            )
        ],
        item_dtos=[],
        brand_dtos=[])

    #Act
    form_details_dto = form_storage.get_form_details_dto(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details_dto == expected_form_details_dto


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_forms_details_dto_when_no_sections_exists_returns_empty_list_of_sections_items_and_brands(
        forms):
    #Arrange
    form_id = 1
    user_id = 1
    form_storage = FormStorageImplementation()
    expected_form_details_dto = FormDetailsDto(
        form_id=1, form_description='This is snacks form',
        form_name='Snacks Form',
        close_date=datetime.datetime(2020, 6, 7, 5, 4, 3),
        section_dtos=[], item_dtos=[], brand_dtos=[]
    )

    #Act
    form_details_dto = form_storage.get_form_details_dto(
        form_id=form_id, user_id=user_id
    )

    #Assert
    assert form_details_dto == expected_form_details_dto
