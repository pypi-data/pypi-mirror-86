import pytest
from django_swagger_utils.drf_server.exceptions import NotFound
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.constants.exception_messages \
    import INVALID_ITEM_EXCEPTION


def test_raise_invalid_item_id_exception():
    #Arrange
    json_presenter = PresenterImplementation()
    expected_exception_message = INVALID_ITEM_EXCEPTION[0]
    expected_exception_res_status = INVALID_ITEM_EXCEPTION[1]

    #Act
    with pytest.raises(NotFound) as exception:
        json_presenter.raise_invalid_item_id_exception()

    #Assert
    assert exception.value.message == expected_exception_message
    assert exception.value.res_status == expected_exception_res_status
