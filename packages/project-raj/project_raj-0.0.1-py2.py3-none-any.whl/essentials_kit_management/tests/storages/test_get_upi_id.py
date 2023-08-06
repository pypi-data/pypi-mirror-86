import pytest
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.models import BankDetails


@pytest.mark.django_db
def test_get_upi_id_returns_upi_id(users):
    #Arrange
    storage = StorageImplementation()
    expected_upi_id = "8247088772@SBI"
    BankDetails.objects.create(upi_id="8247088772@SBI")
    
    #Act
    upi_id = storage.get_upi_id()
    
    #Assert
    assert upi_id == expected_upi_id
