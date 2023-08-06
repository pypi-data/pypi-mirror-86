import pytest
import datetime
from freezegun import freeze_time
from oauth2_provider.models import AccessToken
from essentials_kit_management.constants.enums \
    import StatusEnum, TransactionTypeEnum, VerificationChoicesEnum
from essentials_kit_management.models \
    import User, Form, Section, Brand, OrderItem, \
    Item, Transaction, BankDetails
from essentials_kit_management.interactors.storages.dtos import ItemDto
from essentials_kit_management.interactors.dtos import PostItemDetailsDto


@pytest.fixture()
def users():
    users_list = [
            User(username="Rajesh", name="Rajesh"),
            User(username="Kumar", name="Rajesh"),
            User(username="RajKumar", name="Rajesh")
        ]
    User.objects.bulk_create(users_list)
    users = User.objects.all()
    users = list(users)
    for user in users:
        user.set_password('admin123')
        user.save()
    return users


@pytest.fixture()
@freeze_time("2020-05-17 20:22:46")
def sections(forms):
    sections_list = [
        Section(title="Snack Items", description="SnacksSec", form_id=1),
        Section(title="Biscuits", description="BiscuitsSec", form_id=1),
    ]
    Section.objects.bulk_create(sections_list)
    sections = Section.objects.all()
    return sections


@pytest.fixture()
@freeze_time("2020-05-17 20:22:46")
def forms(users):
    forms_list = [
        Form(
            description="This is snacks form", name="Snacks Form",
            status=StatusEnum.LIVE.value,
            close_date=datetime.datetime(2020, 6, 7, 5, 4, 3)
        ),
        Form(
            description="This is accomodation form", name="Acco Form",
            status=StatusEnum.CLOSED.value,
            expected_delivery_date=None
        )
    ]
    Form.objects.bulk_create(forms_list)
    forms = Form.objects.all()
    users = User.objects.all()
    for form in forms:
        for user in users:
            form.users.add(user)
    return forms


@pytest.fixture()
@freeze_time("2020-05-17 20:22:46")
def items(sections):
    items_list = [
        Item(name="Navaratna", description="50 mg", section_id=1),
        Item(name="Moong Dal", description="100 mg", section_id=1),
    ]
    Item.objects.bulk_create(items_list)
    items = Item.objects.all()
    return items


@pytest.fixture()
@freeze_time("2020-05-17 20:22:46")
def brands():
    brands_list = [
        Brand(
            name="XXXX", min_quantity="10",
            max_quantity=20, price=200, item_id=1
        ),
        Brand(
            name="YYYY", min_quantity="5",
            max_quantity=10, price=100, item_id=1
        ),
        Brand(
            name="ZZZZ", min_quantity="2",
            max_quantity=20, price=100, item_id=1
        )
    ]
    Brand.objects.bulk_create(brands_list)
    brands = Brand.objects.all()
    return brands


@pytest.fixture()
def ordered_items(users, items, brands):
    ordered_items_list = [
        OrderItem(
            user_id=1, item_id=1, brand_id=2, ordered_quantity=10,
            delivered_quantity=7, is_out_of_stock=True
        ),
        OrderItem(
            user_id=1, item_id=2, brand_id=1, ordered_quantity=7,
            delivered_quantity=7, is_out_of_stock=False
        )
    ]
    OrderItem.objects.bulk_create(ordered_items_list)
    ordered_items = OrderItem.objects.all()
    return ordered_items


@pytest.fixture()
def get_item_details_dtos():
    item_details_dtos = [
        PostItemDetailsDto(
            item_id=1, brand_id=1, ordered_quantity=5
        ),
        PostItemDetailsDto(
            item_id=2, brand_id=3, ordered_quantity=7
        )
    ]
    return item_details_dtos


@pytest.fixture()
@freeze_time("2020-05-17 20:22:46")
def transactions(users):
    transactions_list = [
        Transaction(
            payment_transaction_id="12374u3uy34",
            transaction_type=TransactionTypeEnum.PHONE_PAY.value,
            credit_amount=1000.0, screenshot_url="https://google.com",
            remarks="Snacks Form", user_id=1,
            verification_status=VerificationChoicesEnum.APPROVED.value,
        ),
        Transaction(
            payment_transaction_id=None,
            transaction_type=None,
            debit_amount=100.0, screenshot_url=None,
            remarks="Wallet", user_id=1,
            verification_status=None,
        )
    ]
    Transaction.objects.bulk_create(transactions_list)
    transactions = Transaction.objects.all()
    return transactions


@pytest.fixture()
def access_tokens(users):
    access_tokens_list = [
        AccessToken(
            token="jsdfbjherbfgvjb", user_id=1,
            expires=datetime.datetime(2050, 5, 9, 3, 4, 2)
        ),
        AccessToken(
            token="skhfdbshjdbfjhk", user_id=2,
            expires=datetime.datetime(2050, 5, 9, 3, 4, 2)
        )
    ]
    AccessToken.objects.bulk_create(access_tokens_list)
    access_tokens = AccessToken.objects.all()
    return access_tokens


@pytest.fixture()
def item_dtos():
    item_dtos = [
        ItemDto(
            item_id=1, section_id=1, item_name='Cadbury',
            item_description='chocolate'
        ),
        ItemDto(
            item_id=2, section_id=2, item_name='Milk',
            item_description='Milk'
        )
    ]
    return item_dtos
