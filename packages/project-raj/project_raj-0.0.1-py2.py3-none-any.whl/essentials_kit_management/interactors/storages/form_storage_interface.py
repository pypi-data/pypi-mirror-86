from typing import List
from abc import abstractmethod, ABC
from essentials_kit_management.interactors.storages.dtos \
    import FormDto, FormDetailsDto


class FormStorageInterface(ABC):

    @abstractmethod
    def get_forms_details_as_list(
            self, offset: int, limit: int) -> List[FormDto]:
        pass

    @abstractmethod
    def get_total_forms_count(self):
        pass

    @abstractmethod
    def update_form_status(self, form_id: int, status_value: str):
        pass

    @abstractmethod
    def get_form_details_dto(
            self, form_id: int, user_id: int) -> FormDetailsDto:
        pass

    @abstractmethod
    def validate_form_id(self, form_id: int) -> bool:
        pass
