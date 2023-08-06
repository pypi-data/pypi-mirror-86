from django_swagger_utils.utils.test import CustomAPITestCase
from essentials_kit_management.tests.factories.factories import \
    UserFactory, FormFactory, BrandFactory, ItemFactory, SectionFactory, \
    OrderItemFactory, TransactionFactory, BankDetailsFactory


def create_users():
    UserFactory.create_batch(size=10)


def create_brands():
    BrandFactory.create_batch(size=100)
    

def create_items_and_their_brands():
    ItemFactory.create_batch(size=50)
    create_brands()


def create_sections_along_with_items():
    SectionFactory.create_batch(size=20)
    create_items_and_their_brands()


def create_order_items():
    OrderItemFactory.create_batch(size=10)


def create_complete_forms():
    FormFactory.create_batch(size=20)
    create_sections_along_with_items()
    create_order_items()


class CustomUtilsAPI(CustomAPITestCase):
 
    def setupUser(self, username, password):
        UserFactory.reset_sequence()
        BrandFactory.reset_sequence()
        ItemFactory.reset_sequence()
        SectionFactory.reset_sequence()
        TransactionFactory.reset_sequence()
        BankDetailsFactory.reset_sequence()
        FormFactory.reset_sequence()
        OrderItemFactory.reset_sequence()
        super(CustomUtilsAPI, self).setupUser(
            username=username, password=password
        )
