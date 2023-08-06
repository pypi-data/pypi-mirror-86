import json
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
import json
from django.http import HttpResponse
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.\
    get_pay_through_details_interactor import GetPayThroughDetailsInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):

    storage = StorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetPayThroughDetailsInteractor(
        storage=storage, presenter=presenter
    )

    upi_id_response = interactor.get_pay_through_details()

    response = json.dumps(upi_id_response)

    return HttpResponse(response, status=200)
