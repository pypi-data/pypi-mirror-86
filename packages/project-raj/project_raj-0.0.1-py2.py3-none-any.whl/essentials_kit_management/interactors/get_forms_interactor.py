import datetime
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.storages.dtos \
    import FormsListMetricsDto, CompleteFormsDetailsDto
from essentials_kit_management.constants.enums import StatusEnum


class GetFormsInteractor:

    def __init__(
            self, form_storage: FormStorageInterface,
            order_item_storage: OrderItemStorageInterface,
            presenter: PresenterInterface):
        self.form_storage = form_storage
        self.order_item_storage = order_item_storage
        self.presenter = presenter

    def get_forms_as_list(self, user_id: int, offset: int, limit: int):
        form_dtos = \
            self.form_storage.get_forms_details_as_list(
                offset=offset, limit=limit
            )
        user_ordered_item_dtos = \
            self.order_item_storage.get_ordered_items_dtos_of_user(
                user_id=user_id
            )
        forms_list_metrics_dtos = \
            self._get_forms_metrics_dtos(form_dtos, user_ordered_item_dtos)
        updated_form_dtos = \
            self._change_forms_status_if_present_status_expires(
                form_dtos, forms_list_metrics_dtos
            )
        total_forms_count = self.form_storage.get_total_forms_count()

        forms_details = CompleteFormsDetailsDto(
            total_forms_count=total_forms_count,
            form_dtos=updated_form_dtos,
            ordered_item_dtos=user_ordered_item_dtos
        )

        complete_forms_details = self.presenter.get_forms_details_response(
            forms_details=forms_details,
            forms_list_metrics_dtos=forms_list_metrics_dtos,
        )
        return complete_forms_details

    def _get_forms_metrics_dtos(self, form_dtos, ordered_item_dtos):
        form_metrics_dtos = []
        for form_dto in form_dtos:
            form_id = form_dto.form_id
            form_metrics_dto = \
                self._get_metrics_of_form_as_dto(form_id, ordered_item_dtos)
            form_metrics_dtos.append(form_metrics_dto)
        return form_metrics_dtos

    def _get_metrics_of_form_as_dto(self, form_id, ordered_item_dtos):
        ordered_item_dtos_of_form = \
            self._get_filtered_ordered_items_of_form(
                form_id, ordered_item_dtos
            )
        items_count = self._get_items_count(ordered_item_dtos_of_form)
        estimated_cost = self._get_estimated_price(ordered_item_dtos_of_form)
        items_pending = \
            self._get_items_yet_to_deliver(ordered_item_dtos_of_form)
        cost_incurred = \
            self._get_cost_incurred(ordered_item_dtos_of_form)

        form_metrics_dto = FormsListMetricsDto(
            form_id=form_id, items_count=items_count,
            estimated_cost=estimated_cost, items_pending=items_pending,
            cost_incurred=cost_incurred
        )
        return form_metrics_dto

    def _get_items_yet_to_deliver(self, item_dtos):
        items_pending_count = 0
        for item_dto in item_dtos:
            is_pending_item = self._check_is_pending_item(item_dto)
            if is_pending_item:
                items_pending_count = \
                    items_pending_count + item_dto.ordered_quantity - \
                    item_dto.delivered_quantity
        return items_pending_count

    def _get_cost_incurred(self, item_dtos):
        cost_incurred = 0
        for item_dto in item_dtos:
            total_item_cost_delivered = \
                item_dto.item_price * item_dto.delivered_quantity
            cost_incurred = cost_incurred + total_item_cost_delivered
        return cost_incurred

    def _check_is_pending_item(self, item_dto):
        is_item_delivered = self._check_is_item_delivered(item_dto)
        is_item_not_delivered = not is_item_delivered
        is_pending_item = is_item_not_delivered or item_dto.is_out_of_stock
        return is_pending_item

    def _change_forms_status_if_present_status_expires(
            self, form_dtos, forms_list_metrics_dtos):
        updated_form_dtos = []
        for form_dto, metrics_dto in zip(form_dtos, forms_list_metrics_dtos):
            form_dto = self._check_and_update_status(form_dto, metrics_dto)
            updated_form_dtos.append(form_dto)
        return updated_form_dtos

    def _check_and_update_status(self, form_dto, metrics_dto):

        is_valid_close_date = \
            self._check_is_valid_datetime(form_dto.close_date)

        if is_valid_close_date:
            is_form_closed = datetime.datetime.now() >= form_dto.close_date
            if is_form_closed:
                status_value = StatusEnum.CLOSED.value
                form_dto.form_status = status_value

        is_present_status_closed = \
            form_dto.form_status == StatusEnum.CLOSED.value
        is_all_items_delivered = not metrics_dto.items_pending
        is_form_contains_orders = metrics_dto.items_count
        is_delivery_done = \
            is_form_contains_orders and is_present_status_closed and \
            is_all_items_delivered

        if is_delivery_done:
            status_value = StatusEnum.DONE.value
            form_dto.form_status = status_value
            return form_dto

        is_delivery_pending = \
            is_form_contains_orders and is_present_status_closed

        if is_delivery_pending:
            form_dto.expected_delivery_date = datetime.datetime(
                2020, 8, 9, 2, 3, 1
            )

        return form_dto

    @staticmethod
    def _check_is_valid_datetime(datetime_obj):
        is_invalid_datetime = datetime_obj is None
        is_valid_datetime = not is_invalid_datetime
        return is_valid_datetime

    @staticmethod
    def _get_items_count(ordered_item_dtos):
        items_count = 0
        for ordered_item_dto in ordered_item_dtos:
            items_count = items_count + ordered_item_dto.ordered_quantity
        return items_count

    @staticmethod
    def _check_is_item_delivered(item_dto):
        is_item_delivered = \
            item_dto.ordered_quantity == item_dto.delivered_quantity
        return is_item_delivered

    @staticmethod
    def _get_estimated_price(item_dtos):
        estimated_cost = 0
        for item_dto in item_dtos:
            total_item_cost = item_dto.item_price * item_dto.ordered_quantity
            estimated_cost = estimated_cost + total_item_cost
        return estimated_cost

    @staticmethod
    def _get_filtered_ordered_items_of_form(form_id, item_dtos):
        item_dtos_of_form = [
            item_dto
            for item_dto in item_dtos
            if form_id == item_dto.form_id
        ]
        return item_dtos_of_form
