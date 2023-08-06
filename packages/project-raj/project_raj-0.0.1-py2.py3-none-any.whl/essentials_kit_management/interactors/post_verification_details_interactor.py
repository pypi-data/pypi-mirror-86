from typing import Dict
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.exceptions.exceptions \
    import InvalidValueException
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.dtos \
    import PostVerificationDetailsDto


class PostVerificationDetailsInteractor:
    def __init__(
            self, storage: StorageInterface, presenter: PresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def post_verification_details(
            self, user_id: int, verification_details: Dict):
        amount = verification_details['amount']

        try:
            self._check_is_positive(amount)
        except InvalidValueException:
            self.presenter.raise_invalid_value_exception()
            return

        verification_details_dto = \
            self._convert_verification_details_into_dto(
                verification_details
            )
        self.storage.create_transaction_request(
            user_id=user_id,
            verification_details_dto=verification_details_dto
        )

        self.presenter.post_verification_details_response()
        return

    @staticmethod
    def _convert_verification_details_into_dto(verification_details):
        amount = verification_details['amount']
        payment_transaction_id = \
            verification_details['payment_transaction_id']
        transaction_type = verification_details['transaction_type']
        screenshot_url = verification_details['screenshot_url']

        verification_details_dto = PostVerificationDetailsDto(
            amount=amount,
            payment_transaction_id=payment_transaction_id,
            transaction_type=transaction_type,
            screenshot_url=screenshot_url
        )
        return verification_details_dto

    @staticmethod
    def _check_is_positive(value):
        is_positive = value > 0
        is_invalid = not is_positive
        if is_invalid:
            raise InvalidValueException
