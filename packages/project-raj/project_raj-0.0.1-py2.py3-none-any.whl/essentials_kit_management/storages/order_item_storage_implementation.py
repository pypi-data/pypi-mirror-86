from typing import List
from django.db.models import Prefetch
from essentials_kit_management.models \
    import OrderItem, Form, Item, Section, Brand, User
from essentials_kit_management.interactors.storages.\
    order_item_storage_interface import OrderItemStorageInterface
from essentials_kit_management.interactors.storages.dtos \
    import OrderedItemDto, ItemDto, UserOrderDetailsDto
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


class OrderItemStorageImplementation(OrderItemStorageInterface):

    def validate_form_id(self, form_id: int) -> bool:
        is_valid_form = Form.objects.filter(id=form_id).exists()
        return is_valid_form

    def get_ordered_items_dtos_of_user(
            self, user_id: int) -> List[OrderedItemDto]:
        ordered_items = OrderItem.objects.filter(
            user_id=user_id
        ).prefetch_related('brand', 'item__section')

        ordered_item_dtos = \
            self._convert_ordered_items_into_dtos_list(ordered_items)
        return ordered_item_dtos

    def get_user_ordered_item_dtos_of_form(
            self, item_dtos: List[ItemDto],
            user_id: int) -> List[OrderedItemDto]:
        item_ids_in_item_dtos = [
            item_dto.item_id
            for item_dto in item_dtos
        ]

        ordered_items = OrderItem.objects.filter(
            user_id=user_id, item_id__in=item_ids_in_item_dtos
        ).prefetch_related('item__section', 'brand')

        ordered_items_dtos = self._convert_ordered_items_into_dtos_list(
            ordered_items
        )
        return ordered_items_dtos

    def get_user_ordered_details_dtos_of_form(
            self, form_id: int, user_id: int) -> List[UserOrderDetailsDto]:
        form = self._get_form_with_related_date(form_id)
        form_sections = form.form_sections
        items_of_form = self._get_items_in_all_section(form_sections)
        ordered_items_details = \
            self._get_user_ordered_items_details_from_items(
                items_of_form, user_id
            )
        order_item_details_dtos = self._convert_order_item_details_to_dtos(
            ordered_items_details
        )
        return order_item_details_dtos

    def delete_orders_of_user_for_given_item_ids(
            self, item_ids_to_delete_orders: List[int],
            user_id: int, form_id: int):
        form = self._get_form_with_related_date(form_id)
        form_sections = form.form_sections
        items_of_form = self._get_items_in_all_section(form_sections)
        item_ids_to_delete = [
            item.id
            for item in items_of_form
            if item.id in item_ids_to_delete_orders
        ]
        OrderItem.objects.filter(
            user_id=user_id, item_id__in=item_ids_to_delete
        ).delete()

    def get_existing_item_ids_of_user_in_order_items(
            self, user_id: int) -> List[int]:
        existing_item_ids = OrderItem.objects.filter(
            user_id=user_id
        ).values_list('item_id', flat=True)
        existing_item_ids_list = list(existing_item_ids)
        return existing_item_ids_list

    def create_order_items(
            self, user_id: int, form_id: int,
            item_details_dtos: List[PostItemDetailsDto]):

        order_item_objs = [
            self._convert_item_details_dtos_to_order_objects(
                user_id, item_details_dto
            )
            for item_details_dto in item_details_dtos
        ]
        OrderItem.objects.bulk_create(order_item_objs)

    def update_order_items(
            self, user_id: int, item_details_dtos: List[PostItemDetailsDto],
            item_ids: List[int]):
        orders = OrderItem.objects.filter(item_id__in=item_ids)
        for order in orders:
            for item_details_dto in item_details_dtos:
                is_item_details_dto_belongs_to_oder = \
                    order.item_id == item_details_dto.item_id
                if is_item_details_dto_belongs_to_oder:
                    order.brand_id = item_details_dto.brand_id
                    order.ordered_quantity = item_details_dto.ordered_quantity
                    break
        OrderItem.objects.bulk_update(
            orders, ['brand_id', 'ordered_quantity']
        )

    @staticmethod
    def _get_form_with_related_date(form_id):
        items_query = Item.objects.prefetch_related(
            Prefetch('ordered_items', to_attr='filtered_ordered_items')
        )
        sections_query = Section.objects.prefetch_related(
            Prefetch('items', queryset=items_query, to_attr='section_items')
        )
        form = Form.objects.prefetch_related(
            Prefetch(
                'sections', queryset=sections_query, to_attr='form_sections'
            )
        ).get(id=form_id)
        return form

    @staticmethod
    def _convert_ordered_items_into_dtos_list(ordered_items):
        ordered_item_dtos = [
            OrderedItemDto(
                ordered_item_id=ordered_item.id,
                user_id=ordered_item.user_id,
                item_id=ordered_item.item_id,
                brand_id=ordered_item.brand_id,
                form_id=ordered_item.item.section.form_id,
                item_price=ordered_item.brand.price,
                ordered_quantity=ordered_item.ordered_quantity,
                delivered_quantity=ordered_item.delivered_quantity,
                is_out_of_stock=ordered_item.is_out_of_stock
            )
            for ordered_item in ordered_items
        ]
        return ordered_item_dtos

    @staticmethod
    def _get_items_in_all_section(sections):
        items = []
        for section in sections:
            items_of_section = section.section_items
            items = items + items_of_section
        return items

    @staticmethod
    def _filter_user_ordered_items_from_items(items, user_id):
        ordered_items = OrderItem.objects.filter(
            item_id__in=items, user_id=user_id
        )
        return ordered_items

    @staticmethod
    def _get_user_ordered_items_details_from_items(items, user_id):
        ordered_item_details = OrderItem.objects.filter(
            item_id__in=items, user_id=user_id
        ).select_related('item', 'brand')
        return ordered_item_details

    @staticmethod
    def _convert_item_details_dtos_to_order_objects(
            user_id, item_details_dto):
        item_id = item_details_dto.item_id
        brand_id = item_details_dto.brand_id
        ordered_quantity = item_details_dto.ordered_quantity
        order_item_obj = OrderItem(
            user_id=user_id, item_id=item_id,
            brand_id=brand_id, ordered_quantity=ordered_quantity
        )
        return order_item_obj

    @staticmethod
    def _convert_order_item_details_to_dtos(ordered_items_details):
        ordered_item_details_dtos = [
            UserOrderDetailsDto(
                ordered_item_id=ordered_item_details.id,
                item_id=ordered_item_details.item_id,
                item_name=ordered_item_details.item.name,
                item_price=ordered_item_details.brand.price,
                ordered_quantity=ordered_item_details.ordered_quantity,
                delivered_quantity=ordered_item_details.delivered_quantity,
                is_out_of_stock=ordered_item_details.is_out_of_stock
            )
            for ordered_item_details in ordered_items_details
        ]
        return ordered_item_details_dtos
