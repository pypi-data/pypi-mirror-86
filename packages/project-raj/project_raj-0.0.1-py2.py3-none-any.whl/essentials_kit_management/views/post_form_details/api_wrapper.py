from django.http import HttpResponse
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from essentials_kit_management.storages.storage_implementation \
    import StorageImplementation
from essentials_kit_management.storages.form_storage_implementation \
    import FormStorageImplementation
from essentials_kit_management.storages.order_item_storage_implementation \
    import OrderItemStorageImplementation
from essentials_kit_management.presenters.presenter_implementation \
    import PresenterImplementation
from essentials_kit_management.interactors.post_form_interactor \
    import PostFormInteractor


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.id
    form_id = kwargs['form_id']
    request_data = kwargs['request_data']
    item_details_list = request_data['item_details']
    
    storage = StorageImplementation()
    form_storage = FormStorageImplementation()
    order_item_storage = OrderItemStorageImplementation()
    presenter = PresenterImplementation()
    interactor = PostFormInteractor(
        form_storage=form_storage,
        order_item_storage=order_item_storage,
        storage=storage,
        presenter=presenter
    )

    interactor.post_form_details(
        user_id=user_id, form_id=form_id, item_details_list=item_details_list
    )
    
    return HttpResponse(status=201)
