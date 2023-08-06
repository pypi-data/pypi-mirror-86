import json
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from django.http import HttpResponse
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.get_forms_interactor \
    import GetFormsInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    params_data = kwargs['request_query_params']
    offset = params_data['offset']
    limit = params_data['limit']

    form_storage = FormStorageImplementation()
    order_item_storage = OrderItemStorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetFormsInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    forms_details = interactor.get_forms_as_list(
        user_id=user_id, offset=offset, limit=limit
    )

    response = json.dumps(forms_details)
    return response
