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
from essentials_kit_management.interactors.get_form_interactor \
    import GetFormInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    form_id = kwargs['form_id']
    form_storage = FormStorageImplementation()
    order_item_storage = OrderItemStorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetFormInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        presenter=presenter
    )

    forms_details = interactor.get_form_details(
        form_id=form_id, user_id=user_id
    )
    response = json.dumps(forms_details)
    return response
