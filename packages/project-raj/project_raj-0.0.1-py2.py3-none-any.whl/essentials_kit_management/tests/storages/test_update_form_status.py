import pytest
import datetime
from freezegun import freeze_time
from essentials_kit_management.models import Form
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation
from essentials_kit_management.constants.enums import StatusEnum


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_update_form_status_with_status_value_close(forms):
    #Arrange
    form_id = 1
    status_value = StatusEnum.CLOSED.value
    form_storage = FormStorageImplementation()

    #Act
    form_storage.update_form_status(
        form_id=form_id, status_value=status_value
    )

    #Assert
    form = Form.objects.get(id=form_id)
    assert form.status == status_value


@pytest.mark.django_db
@freeze_time("2020-05-17 20:22:46")
def test_update_form_status_with_status_value_done(forms):
    #Arrange
    form_id = 1
    status_value = StatusEnum.DONE.value
    form_storage = FormStorageImplementation()

    #Act
    form_storage.update_form_status(
        form_id=form_id, status_value=status_value
    )

    #Assert
    form = Form.objects.get(id=form_id)
    assert form.status == status_value
