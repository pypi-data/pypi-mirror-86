from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation


def test_get_pay_through_details_response_returns_upi_id_dict():
    #Arrange
    json_presenter = PresenterImplementation()
    upi_id = "8247088772@SBI"
    expected_upi_id_response = {"upi_id": upi_id}

    #Act
    upi_id_response = json_presenter.get_pay_through_details_response(upi_id)

    #Assert
    assert upi_id_response == expected_upi_id_response
