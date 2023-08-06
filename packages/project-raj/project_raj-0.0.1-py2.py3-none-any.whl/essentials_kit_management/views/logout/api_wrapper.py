from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from django.http import HttpResponse
from essentials_kit_management.storages.user_storage_implementation \
    import UserStorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.logout_interactor \
    import LogoutInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    access_token = kwargs['access_token']
    user_storage = UserStorageImplementation()
    presenter = PresenterImplementation()
    interactor = LogoutInteractor(
        user_storage=user_storage, presenter=presenter
    )

    interactor.logout(access_token=access_token)

    return HttpResponse(status=205)
