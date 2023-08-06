import pytest
import datetime
from freezegun import freeze_time
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation
from essentials_kit_management.interactors.storages.dtos \
    import FormDto
from essentials_kit_management.constants.enums import StatusEnum


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_forms_details_as_list_returns_list_of_dtos(forms):
    #Arrange
    offset = 0
    limit = 10
    form_storage = FormStorageImplementation()
    expected_form_list_dtos = [
        FormDto(
            form_id=1, form_name='Snacks Form',
            form_description='This is snacks form', form_status='LIVE',
            close_date=datetime.datetime(2020, 6, 7, 5, 4, 3),
            expected_delivery_date=None
        ),
        FormDto(
            form_id=2, form_name='Acco Form',
            form_description='This is accomodation form',
            form_status='CLOSED', close_date=None, expected_delivery_date=None
        )
    ]

    #Act
    form_list_dtos = form_storage.get_forms_details_as_list(
        offset=offset, limit=limit
    )

    #Assert
    assert form_list_dtos == expected_form_list_dtos


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_get_forms_details_as_list_when_no_form_exists_returns_empty_list(
        users):
    #Arrange
    offset = 0
    limit = 10
    form_storage = FormStorageImplementation()
    expected_form_list_dtos = []

    #Act
    form_list_dtos = form_storage.get_forms_details_as_list(
        offset=offset, limit=limit
    )

    #Assert
    assert form_list_dtos == expected_form_list_dtos
