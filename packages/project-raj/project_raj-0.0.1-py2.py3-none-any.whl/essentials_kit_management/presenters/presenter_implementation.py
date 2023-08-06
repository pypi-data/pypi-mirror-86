from typing import Dict
from django_swagger_utils.drf_server.exceptions \
    import Forbidden, NotFound, BadRequest, Unauthorized
from common.dtos import UserAuthTokensDTO
from essentials_kit_management.constants.exception_messages \
    import INVALID_USERNAME_EXCEPTION, INVALID_PASSWORD_EXCEPTION, \
    INVALID_FORM_EXCEPTION, INVALID_BRAND_EXCEPTION, INVALID_ITEM_EXCEPTION, \
    INVALID_ACCESS_TOKEN_EXCEPTION, INVALID_VALUE_EXCEPTION
from essentials_kit_management.interactors.presenters.presenter_interface \
    import PresenterInterface
from essentials_kit_management.interactors.storages.dtos \
    import CompleteFormsDetailsDto, FormsListMetricsDto, \
    CompleteFormDetailsDto, FormMetricsDto, OrderDetailsOfFormDto, \
    WalletTransactionDetailsDto, TransactionDetailsDto
from essentials_kit_management.constants.constants \
    import DEFAULT_DATE_TIME_FORMAT


class PresenterImplementation(PresenterInterface):

    def raise_invalid_username_exception(self):
        raise Unauthorized(*INVALID_USERNAME_EXCEPTION)

    def raise_invalid_password_exception(self):
        raise Unauthorized(*INVALID_PASSWORD_EXCEPTION)

    def raise_invalid_form_exception(self):
        raise NotFound(*INVALID_FORM_EXCEPTION)

    def raise_invalid_brand_id_exception(self):
        raise NotFound(*INVALID_BRAND_EXCEPTION)

    def raise_invalid_item_id_exception(self):
        raise NotFound(*INVALID_ITEM_EXCEPTION)

    def raise_invalid_access_token_exception(self):
        raise Unauthorized(*INVALID_ACCESS_TOKEN_EXCEPTION)

    def raise_invalid_value_exception(self):
        raise BadRequest(*INVALID_VALUE_EXCEPTION)

    def post_verification_details_response(self):
        pass

    def post_form_details_response(self):
        pass

    def get_access_token_response(self, access_token_dto: UserAuthTokensDTO):
        access_token_response = {
            "user_id": access_token_dto.user_id,
            "access_token": access_token_dto.access_token,
            "refresh_token": access_token_dto.refresh_token,
            "expires_in": access_token_dto.expires_in
        }
        return access_token_response

    def get_forms_details_response(
            self, forms_details: CompleteFormsDetailsDto,
            forms_list_metrics_dtos: FormsListMetricsDto):
        forms_dtos = forms_details.form_dtos
        forms_in_list_of_dicts = \
            self._get_form_dtos_as_list_of_form_details_dicts(
                forms_dtos, forms_list_metrics_dtos
            )
        forms_complete_details = {
            'forms': forms_in_list_of_dicts,
            'forms_count': forms_details.total_forms_count
        }
        return forms_complete_details

    def get_form_details_response(
            self, complete_form_details_dto: CompleteFormDetailsDto,
            form_metrics_dto: FormMetricsDto):
        complete_form_details_dict = self._get_complete_form_details_dict(
            complete_form_details_dto, form_metrics_dto
        )
        return complete_form_details_dict

    def get_order_details_of_form_response(
            self, ordered_details_of_form_dto: OrderDetailsOfFormDto):
        form_metrics_dto = ordered_details_of_form_dto.form_metrics_dto
        item_metrics_dtos = ordered_details_of_form_dto.item_metrics_dtos

        ordered_details_of_form_response = {
            "form_id": ordered_details_of_form_dto.form_id,
            "order_details": self._get_complete_order_details_list(
                item_metrics_dtos
            ),
            "total_items_count": form_metrics_dto.total_items_count,
            "total_cost_incurred": form_metrics_dto.total_cost_incurred,
            "total_received_items_count":
                form_metrics_dto.total_received_items_count
        }
        return ordered_details_of_form_response

    def get_wallet_transaction_details_response(
            self, wallet_transactions_dto: WalletTransactionDetailsDto):
        wallet_transactions_details = {
            "wallet_balance": wallet_transactions_dto.wallet_balance,
            "transaction_details": self._get_transaction_details_list(
                wallet_transactions_dto.transaction_details_dtos
            )
        }
        return wallet_transactions_details

    def get_pay_through_details_response(self, upi_id: str):
        upi_id_response = {"upi_id": upi_id}
        return upi_id_response

    def logout_response(self):
        pass

    def get_wallet_balance_response(self, wallet_balance: float):
        pass

    def get_transaction_details_response(
            self, transaction_details_dtos: TransactionDetailsDto):
        pass

    def get_wallet_balance_with_transactions_response(
            self,
            wallet_balance_with_transactions_dto: WalletTransactionDetailsDto
    ):
        pass

    def _get_complete_form_details_dict(
            self, complete_form_details_dto, form_metrics_dto):
        form_details_dto = complete_form_details_dto.form_details_dto
        section_dtos = form_details_dto.section_dtos
        item_dtos = form_details_dto.item_dtos
        brand_dtos = form_details_dto.brand_dtos
        ordered_item_dtos = complete_form_details_dto.ordered_item_dtos

        complete_form_details_dict = {
            'form_id': form_details_dto.form_id,
            "form_name": form_details_dto.form_name,
            'form_description': form_details_dto.form_description,
            'close_date': self._convert_valid_datetime_into_string(
                form_details_dto.close_date
            ),
            'sections': self._get_complete_sections_details_as_list_of_dicts(
                section_dtos, item_dtos, brand_dtos, ordered_item_dtos
            ),
            'total_cost': form_metrics_dto.total_cost,
            'total_items': form_metrics_dto.total_items
        }
        return complete_form_details_dict

    def _get_complete_sections_details_as_list_of_dicts(
            self, section_dtos, item_dtos, brand_dtos, ordered_item_dtos):
        section_details_list = []
        for section_dto in section_dtos:
            sections_details_dict = {
                'section_id': section_dto.section_id,
                'section_name': section_dto.product_title,
                'section_description': section_dto.product_description,
                'item_details':
                    self._get_complete_items_details_as_list_of_dicts(
                        section_dto.section_id, item_dtos, brand_dtos,
                        ordered_item_dtos
                    )
            }
            section_details_list.append(sections_details_dict)
        return section_details_list

    def _get_complete_items_details_as_list_of_dicts(
            self, section_id, item_dtos, brand_dtos, ordered_item_dtos):
        item_details_list = []
        for item_dto in item_dtos:
            is_section_item = section_id == item_dto.section_id
            if is_section_item:
                item_details_dict = {
                    'item_id': item_dto.item_id,
                    'item_name': item_dto.item_name,
                    'item_description': item_dto.item_description,
                    'item_brands': self._get_brand_details_as_list_of_dicts(
                        item_dto.item_id, brand_dtos
                    ),
                    'order_details': self._get_order_details_of_item(
                        item_dto.item_id, ordered_item_dtos
                    )
                }
                item_details_list.append(item_details_dict)
        return item_details_list

    def _get_form_dtos_as_list_of_form_details_dicts(
            self, forms_dtos, forms_list_metrics_dtos):
        forms_in_list_of_dicts = []
        for form_dto in forms_dtos:
            form_metrics_dto = self._get_form_metrics_dto(
                form_dto.form_id, forms_list_metrics_dtos
            )

            form_details_dict = {
                "form_id": form_dto.form_id,
                "form_name": form_dto.form_name,
                "form_description": form_dto.form_description,
                "form_status": form_dto.form_status,
                "close_date":
                    self._convert_valid_datetime_into_string(
                        form_dto.close_date
                    ),
                "expected_delivery_date":
                    self._convert_valid_datetime_into_string(
                        form_dto.expected_delivery_date
                    ),
                "items_count": form_metrics_dto.items_count,
                "estimated_cost": form_metrics_dto.estimated_cost,
                "items_pending": form_metrics_dto.items_pending,
                "cost_incurred": form_metrics_dto.cost_incurred
            }
            forms_in_list_of_dicts.append(form_details_dict)
        return forms_in_list_of_dicts

    def _get_transaction_details_list(self, transaction_details_dtos):
        transaction_details_list = [
            {
                "transaction_id": transaction_details_dto.transaction_id,
                "transaction_date":
                    self._convert_datetime_into_date(
                        transaction_details_dto.transaction_date
                    ),
                "credit_amount": transaction_details_dto.credit_amount,
                "debit_amount": transaction_details_dto.debit_amount,
                "verification_status":
                    transaction_details_dto.verification_status,
                "remarks": transaction_details_dto.remarks
            }
            for transaction_details_dto in transaction_details_dtos
        ]
        return transaction_details_list

    @staticmethod
    def _get_brand_details_as_list_of_dicts(item_id, brand_dtos):
        brand_details_list = []
        for brand_dto in brand_dtos:
            is_item_brand = item_id == brand_dto.item_id
            if is_item_brand:
                brand_details_dict = {
                    'brand_id': brand_dto.brand_id,
                    'brand_name': brand_dto.brand_name,
                    'item_price': brand_dto.item_price,
                    'min_quantity': brand_dto.min_quantity,
                    'max_quantity': brand_dto.max_quantity
                }
                brand_details_list.append(brand_details_dict)
        return brand_details_list

    @staticmethod
    def _get_form_metrics_dto(form_id, forms_list_metrics_dtos):
        for form_metrics_dto in forms_list_metrics_dtos:
            is_given_form_metrics_dto = form_metrics_dto.form_id == form_id
            if is_given_form_metrics_dto:
                return form_metrics_dto

    @staticmethod
    def _get_order_details_of_item(item_id, ordered_item_dtos):
        for ordered_item_dto in ordered_item_dtos:
            is_item_ordered = ordered_item_dto.item_id == item_id

            if is_item_ordered:
                order_details_dict = {
                    'brand_id': ordered_item_dto.brand_id,
                    'item_price': ordered_item_dto.item_price,
                    'ordered_quantity': ordered_item_dto.ordered_quantity,
                    'delivered_quantity': ordered_item_dto.delivered_quantity,
                    'is_out_of_stock': ordered_item_dto.is_out_of_stock
                }
                return order_details_dict
        return

    @staticmethod
    def _convert_valid_datetime_into_string(datetime_obj):
        if datetime_obj is None:
            return None
        is_datetime_is_string = type(datetime_obj) == str
        if is_datetime_is_string:
            return datetime_obj
        datetime = datetime_obj.strftime(DEFAULT_DATE_TIME_FORMAT)
        return datetime

    @staticmethod
    def _get_complete_order_details_list(item_metrics_dtos):
        complete_order_details_list = [
            {
                "item_id": item_metrics_dto.item_id,
                "item_name": item_metrics_dto.item_name,
                "quantity_added_for_item":
                    item_metrics_dto.quantity_added_for_item,
                "cost_incurred_for_item":
                    item_metrics_dto.cost_incurred_for_item,
                "quantity_received_for_item":
                    item_metrics_dto.quantity_received_for_item,
                "is_out_of_stock": item_metrics_dto.is_out_of_stock
            }
            for item_metrics_dto in item_metrics_dtos
        ]

        return complete_order_details_list

    @staticmethod
    def _convert_datetime_into_date(datetime_obj):
        date = datetime_obj.strftime("%d %B %Y")
        return date
