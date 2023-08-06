from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.storages.dtos \
    import OrderedFormMetricsDto, ItemMetricsDto, OrderDetailsOfFormDto


class GetOrderDetailsOfFormInteractor:

    def __init__(
            self, order_item_storage: OrderItemStorageInterface,
            form_storage: FormStorageInterface,
            presenter: PresenterInterface):
        self.order_item_storage = order_item_storage
        self.form_storage = form_storage
        self.presenter = presenter

    def get_order_details_of_form(
            self, user_id: int, form_id: int) -> OrderDetailsOfFormDto:
        is_valid_form_id = self.form_storage.validate_form_id(
            form_id=form_id
        )

        is_invalid_form_id = not is_valid_form_id
        if is_invalid_form_id:
            self.presenter.raise_invalid_form_exception()
            return

        ordered_item_dtos = \
            self.order_item_storage.get_user_ordered_details_dtos_of_form(
                form_id=form_id, user_id=user_id
            )
        form_metrics_dto = self._get_form_metrics_dtos(ordered_item_dtos)
        item_metrics_dtos = self._get_item_metrics_dtos(ordered_item_dtos)
        ordered_details_of_form_dto = OrderDetailsOfFormDto(
            form_id=form_id,
            item_metrics_dtos=item_metrics_dtos,
            form_metrics_dto=form_metrics_dto
        )

        ordered_details_of_form = \
            self.presenter.get_order_details_of_form_response(
                ordered_details_of_form_dto=ordered_details_of_form_dto
            )
        return ordered_details_of_form

    def _get_form_metrics_dtos(self, ordered_item_dtos):
        total_items_count = self._get_items_count(ordered_item_dtos)
        total_cost_incurred = self._get_total_cost_incurred(
            ordered_item_dtos
        )
        total_received_items_count = self._get_total_received_items_count(
            ordered_item_dtos
        )
        form_metrics_dto = OrderedFormMetricsDto(
            total_items_count=total_items_count,
            total_cost_incurred=total_cost_incurred,
            total_received_items_count=total_received_items_count
        )
        return form_metrics_dto

    def _get_item_metrics_dtos(self, ordered_item_dtos):
        item_metrics_dtos = [
            self._get_item_metrics_dto(ordered_item_dto)
            for ordered_item_dto in ordered_item_dtos
        ]
        return item_metrics_dtos

    @staticmethod
    def _get_total_cost_incurred(ordered_item_dtos):
        total_cost_incurred = 0
        for ordered_item_dto in ordered_item_dtos:
            total_item_cost = \
                ordered_item_dto.delivered_quantity * \
                ordered_item_dto.item_price
            total_cost_incurred = total_cost_incurred + total_item_cost
        return total_cost_incurred

    @staticmethod
    def _get_items_count(ordered_item_dtos):
        items_count = 0
        for ordered_item_dto in ordered_item_dtos:
            items_count = items_count + ordered_item_dto.ordered_quantity
        return items_count

    @staticmethod
    def _get_total_received_items_count(ordered_item_dtos):
        total_received_items_count = 0
        for ordered_item_dto in ordered_item_dtos:
            total_received_items_count = \
                total_received_items_count + \
                ordered_item_dto.delivered_quantity
        return total_received_items_count

    @staticmethod
    def _get_item_metrics_dto(ordered_item_dto):
        cost_incurred_for_item = \
            ordered_item_dto.item_price * ordered_item_dto.delivered_quantity

        order_item_metrics_dto = ItemMetricsDto(
            item_id=ordered_item_dto.item_id,
            item_name=ordered_item_dto.item_name,
            quantity_added_for_item=ordered_item_dto.ordered_quantity,
            cost_incurred_for_item=cost_incurred_for_item,
            quantity_received_for_item=ordered_item_dto.delivered_quantity,
            is_out_of_stock=ordered_item_dto.is_out_of_stock
        )
        return order_item_metrics_dto
