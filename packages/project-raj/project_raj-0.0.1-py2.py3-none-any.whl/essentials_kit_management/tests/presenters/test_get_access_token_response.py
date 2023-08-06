import datetime
from common.dtos import UserAuthTokensDTO
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation


def test_get_access_token_response_returns_access_token():
    #Arrange
    access_token_dto = UserAuthTokensDTO(
        user_id=1, access_token='KQDt2vRGfdlgCxD8JnUG3rOa63u5tb',
        refresh_token='hpC1itwrO7X4AgjWdOVCLUfJC9P7CE',
        expires_in=datetime.datetime(2337, 4, 16, 16, 58, 0, 32454)
    )
    json_presenter = PresenterImplementation()
    expected_access_token_response = {
        "user_id": access_token_dto.user_id,
        "access_token": access_token_dto.access_token,
        "refresh_token": access_token_dto.refresh_token,
        "expires_in": access_token_dto.expires_in
    }

    #Act
    access_token_response = \
        json_presenter.get_access_token_response(access_token_dto)

    #Assert
    assert access_token_response == expected_access_token_response
