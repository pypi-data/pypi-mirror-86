from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from django.http import HttpResponse
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.\
    post_verification_details_interactor \
    import PostVerificationDetailsInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    request_data = kwargs['request_data']
    verification_details = request_data['verification_details']

    storage = StorageImplementation()
    presenter = PresenterImplementation()
    interactor = PostVerificationDetailsInteractor(
        storage=storage, presenter=presenter
    )

    interactor.post_verification_details(
        user_id=user_id, verification_details=verification_details
    )

    return HttpResponse(status=201)
