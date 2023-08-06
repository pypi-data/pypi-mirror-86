import json
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from django.http import HttpResponse
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.\
    get_wallet_transactions_details_interactor \
    import GetWalletTransactionsDetailsInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    params_data = kwargs['request_query_params']
    offset = params_data['offset']
    limit = params_data['limit']
    storage = StorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetWalletTransactionsDetailsInteractor(
        storage=storage, presenter=presenter
    )
    
    wallet_transactions_details = \
        interactor.get_wallet_transactions_details(
            user_id=user_id, offset=offset, limit=limit
        )

    response = json.dumps(wallet_transactions_details)
    return response
