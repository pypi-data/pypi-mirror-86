from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface


class GetPayThroughDetailsInteractor:
    def __init__(
            self, storage: StorageInterface, presenter: PresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def get_pay_through_details(self):
        upi_id = self.storage.get_upi_id()
        pay_through_details_response = \
            self.presenter.get_pay_through_details_response(upi_id=upi_id)

        return pay_through_details_response
