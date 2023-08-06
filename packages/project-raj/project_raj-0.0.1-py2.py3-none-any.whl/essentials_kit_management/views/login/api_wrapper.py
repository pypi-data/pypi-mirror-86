import json
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from django.http import HttpResponse
from common.oauth2_storage import OAuth2SQLStorage
from essentials_kit_management.storages.user_storage_implementation \
    import UserStorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.login_interactor \
    import LoginInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    username = request_data['username']
    password = request_data['password']
    storage = UserStorageImplementation()
    presenter = PresenterImplementation()
    oauth_storage = OAuth2SQLStorage()
    interactor = LoginInteractor(
        user_storage=storage,
        presenter=presenter,
        oauth_storage=oauth_storage
    )

    access_token_dict = interactor.login_with_credentials(
        username=username, password=password
    )
    access_token_dict["expires_in"] = str(access_token_dict["expires_in"])
    response_data = json.dumps(access_token_dict)
    return HttpResponse(response_data, status=200)
