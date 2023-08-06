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
from essentials_kit_management.interactors.\
    get_order_details_of_form_interactor \
    import GetOrderDetailsOfFormInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    form_id = kwargs['form_id']

    order_item_storage = OrderItemStorageImplementation()
    form_storage = FormStorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetOrderDetailsOfFormInteractor(
        order_item_storage=order_item_storage,
        form_storage=form_storage,
        presenter=presenter
    )
    
    order_details_of_form = interactor.get_order_details_of_form(
        form_id=form_id, user_id=user_id
    )
    response = json.dumps(order_details_of_form)
    return response
