from typing import List
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.storages.storage_interface \
    import StorageInterface
from essentials_kit_management.interactors.presenters.\
    presenter_interface import PresenterInterface
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


class PostFormInteractor:
    def __init__(
            self, form_storage: FormStorageInterface,
            order_item_storage: OrderItemStorageInterface,
            storage: StorageInterface,
            presenter: PresenterInterface):
        self.form_storage = form_storage
        self.order_item_storage = order_item_storage
        self.storage = storage
        self.presenter = presenter

    def post_form_details(
            self, user_id: int, form_id: int, item_details_list: List):
        is_valid_form_id = self.form_storage.validate_form_id(form_id=form_id)
        is_invalid_form_id = not is_valid_form_id
        if is_invalid_form_id:
            self.presenter.raise_invalid_form_exception()

        item_ids = self._get_item_ids_list(item_details_list)
        brand_ids = self._get_brand_ids_list(item_details_list)
        is_item_ids_valid = self._validate_item_ids(item_ids)

        is_item_ids_invalid = not is_item_ids_valid
        if is_item_ids_invalid:
            self.presenter.raise_invalid_item_id_exception()
            return

        is_brand_ids_valid = self._validate_brand_ids(brand_ids)
        is_brand_ids_invalid = not is_brand_ids_valid
        if is_brand_ids_invalid:
            self.presenter.raise_invalid_brand_id_exception()
            return

        existing_item_ids_of_user_orders = self.order_item_storage.\
            get_existing_item_ids_of_user_in_order_items(user_id=user_id)

        item_ids_to_delete_orders = self._get_item_ids_to_delete_orders(
            existing_item_ids_of_user_orders, item_ids
        )
        item_ids_to_update_orders = self._get_item_ids_to_update_orders(
            existing_item_ids_of_user_orders, item_ids
        )
        item_ids_to_create_new_orders = \
            self._get_item_ids_to_create_new_orders(
                existing_item_ids_of_user_orders, item_ids
            )

        item_details_dtos = \
            self._convert_item_details_to_dtos(item_details_list)
        update_request_order_dtos = self._get_update_request_order_dtos(
            item_ids_to_update_orders, item_details_dtos
        )
        new_order_dtos = self._get_new_order_dtos(
            item_ids_to_create_new_orders, item_details_dtos
        )

        self.order_item_storage.delete_orders_of_user_for_given_item_ids(
            user_id=user_id, form_id=form_id,
            item_ids_to_delete_orders=item_ids_to_delete_orders
        )

        if new_order_dtos:
            self.order_item_storage.create_order_items(
                user_id=user_id, form_id=form_id,
                item_details_dtos=new_order_dtos
            )

        if update_request_order_dtos:
            self.order_item_storage.update_order_items(
                user_id=user_id,
                item_ids=item_ids_to_update_orders,
                item_details_dtos=update_request_order_dtos
            )
        self.presenter.post_form_details_response()
        return

    def _validate_item_ids(self, item_ids):
        item_ids_in_db = self.storage.get_item_ids_from_db_if_given_ids_valid(
                item_ids=item_ids
        )
        is_all_ids_valid = sorted(item_ids) == sorted(item_ids_in_db)
        return is_all_ids_valid

    def _validate_brand_ids(self, brand_ids):
        brand_ids_in_db = \
            self.storage.get_brand_ids_from_db_if_given_ids_valid(
                brand_ids=brand_ids
            )
        is_all_ids_valid = sorted(brand_ids) == sorted(brand_ids_in_db)
        return is_all_ids_valid

    @staticmethod
    def _get_item_ids_to_delete_orders(
            existing_item_ids_of_user_orders, item_ids):
        item_ids_to_delete_orders = [
            item_id
            for item_id in existing_item_ids_of_user_orders
            if item_id not in item_ids
        ]
        return item_ids_to_delete_orders

    @staticmethod
    def _get_item_ids_to_update_orders(
            existing_item_ids_of_user_orders, item_ids):
        item_ids_to_update_orders = [
            item_id
            for item_id in existing_item_ids_of_user_orders
            if item_id in item_ids
        ]
        return item_ids_to_update_orders

    @staticmethod
    def _get_item_ids_to_create_new_orders(
            existing_item_ids_of_user_orders, item_ids):
        item_ids_to_create_new_orders = [
            item_id
            for item_id in item_ids
            if item_id not in existing_item_ids_of_user_orders
        ]
        return item_ids_to_create_new_orders

    @staticmethod
    def _convert_item_details_to_dtos(item_details_list):
        post_item_details_dtos = []
        for item_details in item_details_list:
            brand_details = item_details['brand_details']
            post_item_details_dto = PostItemDetailsDto(
                item_id=item_details['item_id'],
                brand_id=brand_details['brand_id'],
                ordered_quantity=item_details['ordered_quantity']
            )
            post_item_details_dtos.append(post_item_details_dto)
        return post_item_details_dtos

    @staticmethod
    def _get_item_ids_list(item_details_list):
        item_ids = [
            item_details['item_id']
            for item_details in item_details_list
        ]
        return item_ids

    @staticmethod
    def _get_brand_ids_list(item_details_list):
        brand_ids = []
        for item_details in item_details_list:
            brand_details = item_details['brand_details']
            brand_id = brand_details['brand_id']
            brand_ids.append(brand_id)
        return brand_ids

    @staticmethod
    def _get_update_request_order_dtos(
            item_ids_to_update_orders, item_details_dtos):
        update_request_order_dtos = [
            item_details_dto
            for item_details_dto in item_details_dtos
            if item_details_dto.item_id in item_ids_to_update_orders
        ]
        return update_request_order_dtos

    @staticmethod
    def _get_new_order_dtos(
            item_ids_to_create_new_orders, item_details_dtos):
        new_order_dtos = [
            item_details_dto
            for item_details_dto in item_details_dtos
            if item_details_dto.item_id in item_ids_to_create_new_orders
        ]
        return new_order_dtos
