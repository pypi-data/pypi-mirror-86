from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.storages.dtos \
    import FormMetricsDto, CompleteFormDetailsDto
from essentials_kit_management.interactors.mixins.form_validation import \
    FormValidationMixin


class GetFormInteractor(FormValidationMixin):
    def __init__(
            self, form_storage: FormStorageInterface,
            order_item_storage: OrderItemStorageInterface,
            presenter: PresenterInterface):
        self.order_item_storage = order_item_storage
        self.form_storage = form_storage
        self.presenter = presenter

    def get_form_details(self, form_id: int, user_id: int):
        self.validate_form_id(form_id=form_id)

        form_details_dto = self.form_storage.get_form_details_dto(
            form_id=form_id, user_id=user_id
        )

        ordered_item_dtos = \
            self.order_item_storage.get_user_ordered_item_dtos_of_form(
                form_details_dto.item_dtos, user_id=user_id
            )

        complete_form_details_dto = \
            CompleteFormDetailsDto(
                form_details_dto=form_details_dto,
                ordered_item_dtos=ordered_item_dtos
            )

        form_metrics_dto = self._get_form_metrics_dtos(
            complete_form_details_dto
        )

        response = self.presenter.get_form_details_response(
            complete_form_details_dto=complete_form_details_dto,
            form_metrics_dto=form_metrics_dto
        )
        return response

    def _get_form_metrics_dtos(self, form_details_dto):
        ordered_items_dtos = form_details_dto.ordered_item_dtos
        total_items = self._get_items_count(ordered_items_dtos)
        total_cost = self._get_total_cost_ordered(
            ordered_items_dtos
        )
        form_metrics_dto = FormMetricsDto(
            total_cost=total_cost,
            total_items=total_items
        )
        return form_metrics_dto

    @staticmethod
    def _get_total_cost_ordered(ordered_items_dtos):
        total_cost = 0
        for item_dto in ordered_items_dtos:
            total_item_cost = \
                item_dto.item_price * item_dto.ordered_quantity
            total_cost = total_cost + total_item_cost
        return total_cost

    @staticmethod
    def _get_items_count(ordered_items_dtos):
        items_count = 0
        for ordered_item_dto in ordered_items_dtos:
            items_count = items_count + ordered_item_dto.ordered_quantity
        return items_count
