import pytest
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation


@pytest.mark.django_db
def test_get_item_ids_from_db_with_valid_ids_returns_list_of_ids(
        users, forms, sections, items):
    #Arrange
    item_ids = [1, 2]
    expected_item_ids_from_db = [1, 2]
    storage = StorageImplementation()

    #Act
    item_ids_from_db = \
        storage.get_item_ids_from_db_if_given_ids_valid(item_ids=item_ids)

    #Assert
    assert item_ids_from_db == expected_item_ids_from_db


@pytest.mark.django_db
def test_get_item_ids_from_db_for_one_invalid_returns_list_of_ids_except_invalid_id(
        users, forms, sections, items):
    #Arrange
    item_ids = [1, 5]
    expected_item_ids_from_db = [1]
    storage = StorageImplementation()

    #Act
    item_ids_from_db = \
        storage.get_item_ids_from_db_if_given_ids_valid(item_ids=item_ids)

    #Assert
    assert item_ids_from_db == expected_item_ids_from_db


@pytest.mark.django_db
def test_get_item_ids_from_db_for_all_invalid_returns_empty_list(
        users, forms, sections, items):
    #Arrange
    item_ids = [9, 10]
    expected_item_ids_from_db = []
    storage = StorageImplementation()

    #Act
    item_ids_from_db = \
        storage.get_item_ids_from_db_if_given_ids_valid(item_ids=item_ids)

    #Assert
    assert item_ids_from_db == expected_item_ids_from_db
