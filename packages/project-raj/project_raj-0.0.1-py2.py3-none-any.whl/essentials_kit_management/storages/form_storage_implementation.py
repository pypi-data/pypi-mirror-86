from typing import List
from django.db.models import Prefetch
from essentials_kit_management.models import Form, Item, Section, User
from essentials_kit_management.interactors.storages.form_storage_interface \
    import FormStorageInterface
from essentials_kit_management.interactors.storages.dtos \
    import FormDto, FormDetailsDto, SectionDto, ItemDto, BrandDto


class FormStorageImplementation(FormStorageInterface):

    def get_forms_details_as_list(
            self, offset: int, limit: int) -> List[FormDto]:
        forms = Form.objects.all()[offset:offset + limit]
        forms_list_dtos = self._convert_forms_into_forms_list_dtos(forms)
        return forms_list_dtos

    def get_total_forms_count(self):
        total_forms_count = Form.objects.all().count()
        return total_forms_count

    def update_form_status(self, form_id: int, status_value: str):
        form = Form.objects.filter(id=form_id).first()
        form.status = status_value
        form.save()

    def get_form_details_dto(
            self, form_id: int, user_id: int) -> FormDetailsDto:
        items_query = Item.objects.prefetch_related(
            Prefetch('brands', to_attr='item_brands')
        )
        sections_query = Section.objects.prefetch_related(
            Prefetch('items', queryset=items_query, to_attr='section_items')
        )
        form = Form.objects.prefetch_related(
            Prefetch(
                'sections', queryset=sections_query, to_attr='form_sections'
            )
        ).get(id=form_id)

        form_details_dto = self._convert_form_into_dto(form)
        return form_details_dto

    def validate_form_id(self, form_id: int) -> bool:
        is_valid_form = Form.objects.filter(id=form_id).exists()
        return is_valid_form

    def _convert_forms_into_forms_list_dtos(self, forms):
        form_list_dtos = []
        for form in forms:
            form_dto = FormDto(
                form_id=form.id, form_name=form.name,
                form_description=form.description, form_status=form.status,
                close_date=form.close_date,
                expected_delivery_date=form.expected_delivery_date
            )
            form_list_dtos.append(form_dto)
        return form_list_dtos

    def _convert_form_into_dto(self, form):
        form_sections = form.form_sections
        section_items = self._get_items_in_all_section(form_sections)
        item_brands = self._get_brands_in_all_items(section_items)

        section_dtos_of_form = self._convert_sections_into_dtos(form_sections)
        item_dtos_of_sections = self._convert_items_into_dtos(section_items)
        brand_dtos_of_items = self._convert_brands_into_dtos(item_brands)

        form_details_dto = FormDetailsDto(
            form_id=form.id,
            form_name=form.name,
            form_description=form.description,
            close_date=form.close_date,
            section_dtos=section_dtos_of_form,
            item_dtos=item_dtos_of_sections,
            brand_dtos=brand_dtos_of_items
        )
        return form_details_dto

    @staticmethod
    def _get_items_in_all_section(sections):
        items = []
        for section in sections:
            items_of_section = section.section_items
            items = items + items_of_section
        return items

    @staticmethod
    def _get_brands_in_all_items(items):
        brands = []
        for item in items:
            brands_of_item = item.item_brands
            brands = brands + brands_of_item
        return brands

    @staticmethod
    def _convert_sections_into_dtos(sections):
        section_dtos = [
            SectionDto(
                section_id=section.id,
                form_id=section.form_id,
                product_title=section.title,
                product_description=section.description
            )
            for section in sections
        ]
        return section_dtos

    @staticmethod
    def _convert_items_into_dtos(items):
        item_dtos = [
            ItemDto(
                item_id=item.id,
                section_id=item.section_id,
                item_name=item.name,
                item_description=item.description,
            )
            for item in items
        ]
        return item_dtos

    @staticmethod
    def _convert_brands_into_dtos(brands):
        brand_dtos = [
            BrandDto(
                brand_id=brand.id,
                item_id=brand.item_id,
                brand_name=brand.name,
                item_price=brand.price,
                min_quantity=brand.min_quantity,
                max_quantity=brand.max_quantity
            )
            for brand in brands
        ]
        return brand_dtos
