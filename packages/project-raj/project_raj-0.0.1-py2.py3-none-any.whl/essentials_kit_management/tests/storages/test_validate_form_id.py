import pytest
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation


@pytest.mark.django_db
def test_validate_form_id_for_valid_id_returns_true(forms):
    #Arrange
    form_id = 1
    form_storage = FormStorageImplementation()

    #Act
    is_valid_form_id = form_storage.validate_form_id(form_id=form_id)

    #Assert
    assert is_valid_form_id is True


@pytest.mark.django_db
def test_validate_form_id_for_invalid_id_returns_false(forms):
    #Arrange
    invalid_form_id = 10
    form_storage = FormStorageImplementation()

    #Act
    is_valid_form_id = form_storage.validate_form_id(form_id=invalid_form_id)

    #Assert
    assert is_valid_form_id is False
