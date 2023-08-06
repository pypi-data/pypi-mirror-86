from typing import List
from abc import abstractmethod, ABC
from essentials_kit_management.interactors.storages.dtos \
    import OrderedItemDto, UserOrderDetailsDto, ItemDto
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


class OrderItemStorageInterface(ABC):

    @abstractmethod
    def get_ordered_items_dtos_of_user(
            self, user_id: int) -> List[OrderedItemDto]:
        pass

    @abstractmethod
    def get_user_ordered_item_dtos_of_form(
            self, item_dtos: List[ItemDto],
            user_id: int) -> List[OrderedItemDto]:
        pass

    @abstractmethod
    def get_user_ordered_details_dtos_of_form(
            self, form_id: int, user_id: int) -> List[UserOrderDetailsDto]:
        pass

    @abstractmethod
    def delete_orders_of_user_for_given_item_ids(
            self, item_ids_to_delete_orders: List[int],
            user_id: int, form_id: int):
        pass

    @abstractmethod
    def create_order_items(
            self, user_id: int, form_id: int,
            item_details_dtos: List[PostItemDetailsDto]):
        pass

    @abstractmethod
    def update_order_items(
            self, user_id: int, item_ids: List[int],
            item_details_dtos: List[PostItemDetailsDto]):
        pass

    @abstractmethod
    def get_existing_item_ids_of_user_in_order_items(
            self, user_id: int) -> List[int]:
        pass

    @abstractmethod
    def validate_form_id(self, form_id: int) -> bool:
        pass
