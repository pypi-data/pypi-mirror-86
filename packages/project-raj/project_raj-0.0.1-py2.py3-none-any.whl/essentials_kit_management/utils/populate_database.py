import datetime
from essentials_kit_management.models \
    import User, Form, Item, Brand, OrderItem, Section, Transaction, \
    BankDetails
from essentials_kit_management.constants.enums \
    import StatusEnum, TransactionTypeEnum, VerificationChoicesEnum


class PopulateDatabase:
    def populate_user_database(self):
        users_list = [
            User(username="Rajesh", name="Rajesh"),
            User(username="Kumar", name="Rajesh"),
            User(username="RajKumar", name="Rajesh")
        ]
        User.objects.bulk_create(users_list)
        users = User.objects.all()
        users[0].set_password("admin123")
        users[1].set_password("admin123")
        users[2].set_password("admin123")
        users[0].save()
        users[1].save()
        users[2].save()

    def populate_forms_database(self):
        forms_list = [
            Form(
                name="Snacks Form",
                description="1. Only one set of Snacks will be given to one individual .Your snacks will not be given to another person .So ,please collect them directly",
                status = StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 10, 15, 4, 3)
            ),
            Form(
                name="Fruits Form",
                description="1. Only one type of Fruits will be given to one individual .Your fruits will not be given to another person .So ,please collect them directly",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 15, 12, 16, 3)
            ),
            Form(
                name="Health Kit",
                description="1. Medicines are limited.Your medicines will not be given to another person .So ,please collect them directly",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 2, 5, 4, 3)
            ),
            Form(
                description="This is snacks form", name="Form 4",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 18, 12, 17, 3)
            ),
            Form(
                description="This is accomodation form", name="Form 5",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 4, 10, 5, 4, 3)
            ),
            Form(
                description="This is fruits form", name="Form 6",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 19, 5, 4, 3)
            ),
            Form(
                description="This is fruits form", name="Form 7",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 5, 10, 5, 4, 3)
            ),
            Form(
                description="This is fruits form", name="Form 8",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 25, 5, 4, 3)
            ),
            Form(
                description="This is fruits form", name="Form 9",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 4, 10, 5, 4, 3)
            ),
            Form(
                description="This is snacks form", name="Form 10",
                status=StatusEnum.LIVE.value,
                close_date=datetime.datetime(2020, 6, 22, 13, 34, 3)
            )
        ]
        Form.objects.bulk_create(forms_list)

    def populate_section_database(self):
        sections_list = [
            Section(title="Chocolates", description="SnacksSec", form_id=1),
            Section(title="Biscuits", description="BiscuitsSec", form_id=1),
            Section(title="Cookies", description="SoapsSec", form_id=1),
            Section(title="Others", description="ToothPaste", form_id=1),
            Section(title="Section 5", description="FruitsSec", form_id=2),
            Section(title="Section 6", description="FruitsSec", form_id=2),
            Section(title="Section 7", description="SnacksSec", form_id=2),
            Section(title="Section 8", description="BiscuitsSec", form_id=2),
            Section(title="Section 9", description="SoapsSec", form_id=3),
            Section(title="Section 10", description="ToothPaste", form_id=3),
            Section(title="Section 11", description="SnacksSec", form_id=3),
            Section(title="Section 12", description="BiscuitsSec", form_id=3),
            Section(title="Section 13", description="SoapsSec", form_id=4),
            Section(title="Section 14", description="ToothPaste", form_id=4),
            Section(title="Section 15", description="FruitsSec", form_id=4),
            Section(title="Section 16", description="FruitsSec", form_id=4),
            Section(title="Section 17", description="SnacksSec", form_id=5),
            Section(title="Section 18", description="BiscuitsSec", form_id=5),
            Section(title="Section 19", description="SoapsSec", form_id=5),
            Section(title="Section 20", description="ToothPaste", form_id=5),
            Section(title="Section 21", description="SnacksSec", form_id=6),
            Section(title="Section 22", description="BiscuitsSec", form_id=6),
            Section(title="Section 23", description="SoapsSec", form_id=6),
            Section(title="Section 24", description="ToothPaste", form_id=6),
            Section(title="Section 25", description="FruitsSec", form_id=7),
            Section(title="Section 26", description="FruitsSec", form_id=7),
            Section(title="Section 27", description="SnacksSec", form_id=7),
            Section(title="Section 28", description="BiscuitsSec", form_id=7),
            Section(title="Section 29", description="SoapsSec", form_id=8),
            Section(title="Section 30", description="ToothPaste", form_id=8),
            Section(title="Section 31", description="SnacksSec", form_id=8),
            Section(title="Section 32", description="BiscuitsSec", form_id=8),
            Section(title="Section 33", description="SoapsSec", form_id=9),
            Section(title="Section 34", description="ToothPaste", form_id=9),
            Section(title="Section 35", description="FruitsSec", form_id=9),
            Section(title="Section 36", description="FruitsSec", form_id=9),
            Section(title="Section 37", description="SnacksSec", form_id=10),
            Section(title="Section 38", description="BiscuitsSec", form_id=10),
            Section(title="Section 39", description="SoapsSec", form_id=10),
            Section(title="Section 40", description="ToothPaste", form_id=10),
        ]
        Section.objects.bulk_create(sections_list)

    def populate_item_database(self):
        items_list = [
            Item(name="Item 1", description="50 mg", section_id=1),
            Item(name="Item 2", description="100 mg", section_id=1),
            Item(name="Item 3", description="a biscuit", section_id=2),
            Item(name="Item 4", description="bisuit", section_id=2),
            Item(name="Item 5", description="100 mg", section_id=3),
            Item(name="Item 6", description="200mg", section_id=3),
            Item(name="Item 7", description="50 mg", section_id=4),
            Item(name="Item 8", description="100 mg", section_id=4),
            Item(name="Item 9", description="fruit", section_id=5),
            Item(name="Item 10", description="fruit", section_id=5),
            Item(name="Item 11", description="50 mg", section_id=6),
            Item(name="Item 12", description="100 mg", section_id=6),
            Item(name="Item 13", description="a biscuit", section_id=7),
            Item(name="Item 14", description="bisuit", section_id=7),
            Item(name="Item 15", description="100 mg", section_id=8),
            Item(name="Item 16", description="200mg", section_id=8),
            Item(name="Item 17", description="50 mg", section_id=9),
            Item(name="Item 18", description="100 mg", section_id=9),
            Item(name="Item 19", description="fruit", section_id=10),
            Item(name="Item 20", description="fruit", section_id=10),
            Item(name="Item 21", description="50 mg", section_id=11),
            Item(name="Item 22", description="100 mg", section_id=11),
            Item(name="Item 23", description="a biscuit", section_id=12),
            Item(name="Item 24", description="bisuit", section_id=12),
            Item(name="Item 25", description="100 mg", section_id=13),
            Item(name="Item 26", description="200mg", section_id=13),
            Item(name="Item 27", description="50 mg", section_id=14),
            Item(name="Item 28", description="100 mg", section_id=14),
            Item(name="Item 29", description="fruit", section_id=15),
            Item(name="Item 30", description="fruit", section_id=15),
            Item(name="Item 31", description="50 mg", section_id=16),
            Item(name="Item 32", description="100 mg", section_id=16),
            Item(name="Item 33", description="a biscuit", section_id=17),
            Item(name="Item 34", description="bisuit", section_id=17),
            Item(name="Item 35", description="100 mg", section_id=18),
            Item(name="Item 36", description="200mg", section_id=18),
            Item(name="Item 37", description="50 mg", section_id=19),
            Item(name="Item 38", description="100 mg", section_id=19),
            Item(name="Item 39", description="fruit", section_id=20),
            Item(name="Item 40", description="fruit", section_id=20),
            Item(name="Item 41", description="50 mg", section_id=21),
            Item(name="Item 42", description="100 mg", section_id=21),
            Item(name="Item 43", description="a biscuit", section_id=22),
            Item(name="Item 44", description="bisuit", section_id=22),
            Item(name="Item 45", description="100 mg", section_id=23),
            Item(name="Item 46", description="200mg", section_id=23),
            Item(name="Item 47", description="50 mg", section_id=24),
            Item(name="Item 48", description="100 mg", section_id=24),
            Item(name="Item 49", description="fruit", section_id=25),
            Item(name="Item 50", description="fruit", section_id=25),
            Item(name="Item 51", description="50 mg", section_id=26),
            Item(name="Item 52", description="100 mg", section_id=26),
            Item(name="Item 53", description="a biscuit", section_id=27),
            Item(name="Item 54", description="bisuit", section_id=27),
            Item(name="Item 55", description="100 mg", section_id=28),
            Item(name="Item 56", description="200mg", section_id=28),
            Item(name="Item 57", description="50 mg", section_id=29),
            Item(name="Item 58", description="100 mg", section_id=29),
            Item(name="Item 59", description="fruit", section_id=30),
            Item(name="Item 60", description="fruit", section_id=30),
            Item(name="Item 61", description="50 mg", section_id=31),
            Item(name="Item 62", description="100 mg", section_id=31),
            Item(name="Item 63", description="a biscuit", section_id=32),
            Item(name="Item 64", description="bisuit", section_id=32),
            Item(name="Item 65", description="100 mg", section_id=33),
            Item(name="Item 66", description="200mg", section_id=33),
            Item(name="Item 67", description="50 mg", section_id=34),
            Item(name="Item 68", description="100 mg", section_id=34),
            Item(name="Item 69", description="50 mg", section_id=35),
            Item(name="Item 70", description="100 mg", section_id=35),
            Item(name="Item 71", description="a biscuit", section_id=36),
            Item(name="Item 72", description="bisuit", section_id=36),
            Item(name="Item 73", description="100 mg", section_id=37),
            Item(name="Item 74", description="200mg", section_id=37),
            Item(name="Item 75", description="50 mg", section_id=38),
            Item(name="Item 76", description="100 mg", section_id=2),
            Item(name="Item 77", description="fruit", section_id=2),
            Item(name="Item 78", description="fruit", section_id=1),
            Item(name="Item 79", description="50 mg", section_id=1),
            Item(name="Item 80", description="100 mg", section_id=1)
        ]
        Item.objects.bulk_create(items_list)
    
    def populate_brand_database(self):
        brands_list = [
            Brand(
                name="Brand 1", min_quantity=10,
                max_quantity=20, price=200, item_id=1
            ),
            Brand(
                name="Brand 2", min_quantity=5,
                max_quantity=10, price=100, item_id=1
            ),
            Brand(
                name="Brand 3", min_quantity=2,
                max_quantity=20, price=100, item_id=2
            ),
            Brand(
                name="Brand 4", min_quantity=10,
                max_quantity=20, price=300, item_id=2
            ),
            Brand(
                name="Brand 5", min_quantity=1,
                max_quantity=10, price=100, item_id=3
            ),
            Brand(
                name="Brand 6", min_quantity=2,
                max_quantity=20, price=100, item_id=3
            ),
            Brand(
                name="Brand 7", min_quantity=10,
                max_quantity=20, price=200, item_id=4
            ),
            Brand(
                name="Brand 8", min_quantity=5,
                max_quantity=10, price=100, item_id=4
            ),
            Brand(
                name="Brand 9", min_quantity=2,
                max_quantity=20, price=100, item_id=5
            ),
            Brand(
                name="Brand 10", min_quantity=10,
                max_quantity=20, price=300, item_id=5
            ),
            Brand(
                name="Brand 11", min_quantity=10,
                max_quantity=20, price=200, item_id=6
            ),
            Brand(
                name="Brand 12", min_quantity=5,
                max_quantity=10, price=100, item_id=6
            ),
            Brand(
                name="Brand 13", min_quantity=2,
                max_quantity=20, price=100, item_id=7
            ),
            Brand(
                name="Brand 14", min_quantity=10,
                max_quantity=20, price=300, item_id=7
            ),
            Brand(
                name="Brand 15", min_quantity=1,
                max_quantity=10, price=100, item_id=8
            ),
            Brand(
                name="Brand 16", min_quantity=2,
                max_quantity=20, price=100, item_id=8
            ),
            Brand(
                name="Brand 17", min_quantity=10,
                max_quantity=20, price=200, item_id=9
            ),
            Brand(
                name="Brand 18", min_quantity=5,
                max_quantity=10, price=100, item_id=9
            ),
            Brand(
                name="Brand 19", min_quantity=2,
                max_quantity=20, price=100, item_id=10
            ),
            Brand(
                name="Brand 20", min_quantity=10,
                max_quantity=20, price=300, item_id=10
            ),
            Brand(
                name="Brand 21", min_quantity=10,
                max_quantity=20, price=200, item_id=11
            ),
            Brand(
                name="Brand 22", min_quantity=5,
                max_quantity=10, price=100, item_id=11
            ),
            Brand(
                name="Brand 23", min_quantity=2,
                max_quantity=20, price=100, item_id=12
            ),
            Brand(
                name="Brand 24", min_quantity=10,
                max_quantity=20, price=300, item_id=12
            ),
            Brand(
                name="Brand 25", min_quantity=1,
                max_quantity=10, price=100, item_id=13
            ),
            Brand(
                name="Brand 26", min_quantity=2,
                max_quantity=20, price=100, item_id=13
            ),
            Brand(
                name="Brand 27", min_quantity=10,
                max_quantity=20, price=200, item_id=14
            ),
            Brand(
                name="Brand 28", min_quantity=5,
                max_quantity=10, price=100, item_id=14
            ),
            Brand(
                name="Brand 29", min_quantity=2,
                max_quantity=20, price=100, item_id=15
            ),
            Brand(
                name="Brand 30", min_quantity=10,
                max_quantity=20, price=300, item_id=15
            ),
            Brand(
                name="Brand 31", min_quantity=10,
                max_quantity=20, price=200, item_id=16
            ),
            Brand(
                name="Brand 32", min_quantity=5,
                max_quantity=10, price=100, item_id=16
            ),
            Brand(
                name="Brand 33", min_quantity=2,
                max_quantity=20, price=100, item_id=17
            ),
            Brand(
                name="Brand 34", min_quantity=10,
                max_quantity=20, price=300, item_id=17
            ),
            Brand(
                name="Brand 35", min_quantity=1,
                max_quantity=10, price=100, item_id=18
            ),
            Brand(
                name="Brand 36", min_quantity=2,
                max_quantity=20, price=100, item_id=18
            ),
            Brand(
                name="Brand 37", min_quantity=10,
                max_quantity=20, price=200, item_id=19
            ),
            Brand(
                name="Brand 38", min_quantity=5,
                max_quantity=10, price=100, item_id=19
            ),
            Brand(
                name="Brand 39", min_quantity=2,
                max_quantity=20, price=100, item_id=20
            ),
            Brand(
                name="Brand 40", min_quantity=10,
                max_quantity=20, price=300, item_id=20
            ),
            Brand(
                name="Brand 41", min_quantity=10,
                max_quantity=20, price=200, item_id=21
            ),
            Brand(
                name="Brand 42", min_quantity=5,
                max_quantity=10, price=100, item_id=21
            ),
            Brand(
                name="Brand 43", min_quantity=2,
                max_quantity=20, price=100, item_id=22
            ),
            Brand(
                name="Brand 44", min_quantity=10,
                max_quantity=20, price=300, item_id=22
            ),
            Brand(
                name="Brand 45", min_quantity=1,
                max_quantity=10, price=100, item_id=23
            ),
            Brand(
                name="Brand 46", min_quantity=2,
                max_quantity=20, price=100, item_id=23
            ),
            Brand(
                name="Brand 47", min_quantity=10,
                max_quantity=20, price=200, item_id=24
            ),
            Brand(
                name="Brand 48", min_quantity=5,
                max_quantity=10, price=100, item_id=24
            ),
            Brand(
                name="Brand 49", min_quantity=2,
                max_quantity=20, price=100, item_id=25
            ),
            Brand(
                name="Brand 50", min_quantity=10,
                max_quantity=20, price=300, item_id=25
            ),
            Brand(
                name="Brand 51", min_quantity=10,
                max_quantity=20, price=200, item_id=26
            ),
            Brand(
                name="Brand 52", min_quantity=5,
                max_quantity=10, price=100, item_id=26
            ),
            Brand(
                name="Brand 53", min_quantity=2,
                max_quantity=20, price=100, item_id=27
            ),
            Brand(
                name="Brand 54", min_quantity=10,
                max_quantity=20, price=300, item_id=27
            ),
            Brand(
                name="Brand 55", min_quantity=1,
                max_quantity=10, price=100, item_id=28
            ),
            Brand(
                name="Brand 56", min_quantity=2,
                max_quantity=20, price=100, item_id=28
            ),
            Brand(
                name="Brand 57", min_quantity=10,
                max_quantity=20, price=200, item_id=29
            ),
            Brand(
                name="Brand 58", min_quantity=5,
                max_quantity=10, price=100, item_id=29
            ),
            Brand(
                name="Brand 59", min_quantity=2,
                max_quantity=20, price=100, item_id=30
            ),
            Brand(
                name="Brand 60", min_quantity=10,
                max_quantity=20, price=300, item_id=30
            ),            Brand(
                name="Brand 61", min_quantity=10,
                max_quantity=20, price=200, item_id=31
            ),
            Brand(
                name="Brand 62", min_quantity=5,
                max_quantity=10, price=100, item_id=31
            ),
            Brand(
                name="Brand 63", min_quantity=2,
                max_quantity=20, price=100, item_id=32
            ),
            Brand(
                name="Brand 64", min_quantity=10,
                max_quantity=20, price=300, item_id=32
            ),
            Brand(
                name="Brand 65", min_quantity=1,
                max_quantity=10, price=100, item_id=33
            ),
            Brand(
                name="Brand 66", min_quantity=2,
                max_quantity=20, price=100, item_id=33
            ),
            Brand(
                name="Brand 67", min_quantity=10,
                max_quantity=20, price=200, item_id=34
            ),
            Brand(
                name="Brand 68", min_quantity=5,
                max_quantity=10, price=100, item_id=34
            ),
            Brand(
                name="Brand 69", min_quantity=2,
                max_quantity=20, price=100, item_id=35
            ),
            Brand(
                name="Brand 70", min_quantity=10,
                max_quantity=20, price=300, item_id=35
            ),            Brand(
                name="Brand 71", min_quantity=10,
                max_quantity=20, price=200, item_id=36
            ),
            Brand(
                name="Brand 72", min_quantity=5,
                max_quantity=10, price=100, item_id=36
            ),
            Brand(
                name="Brand 73", min_quantity=2,
                max_quantity=20, price=100, item_id=37
            ),
            Brand(
                name="Brand 74", min_quantity=10,
                max_quantity=20, price=300, item_id=37
            ),
            Brand(
                name="Brand 75", min_quantity=1,
                max_quantity=10, price=100, item_id=38
            ),
            Brand(
                name="Brand 76", min_quantity=2,
                max_quantity=20, price=100, item_id=38
            ),
            Brand(
                name="Brand 77", min_quantity=10,
                max_quantity=20, price=200, item_id=39
            ),
            Brand(
                name="Brand 78", min_quantity=5,
                max_quantity=10, price=100, item_id=39
            ),
            Brand(
                name="Brand 79", min_quantity=2,
                max_quantity=20, price=100, item_id=40
            ),
            Brand(
                name="Brand 80", min_quantity=10,
                max_quantity=20, price=300, item_id=40
            ),            Brand(
                name="Brand 81", min_quantity=10,
                max_quantity=20, price=200, item_id=41
            ),
            Brand(
                name="Brand 82", min_quantity=5,
                max_quantity=10, price=100, item_id=41
            ),
            Brand(
                name="Brand 83", min_quantity=2,
                max_quantity=20, price=100, item_id=42
            ),
            Brand(
                name="Brand 84", min_quantity=10,
                max_quantity=20, price=300, item_id=42
            ),
            Brand(
                name="Brand 85", min_quantity=1,
                max_quantity=10, price=100, item_id=43
            ),
            Brand(
                name="Brand 86", min_quantity=2,
                max_quantity=20, price=100, item_id=43
            ),
            Brand(
                name="Brand 87", min_quantity=10,
                max_quantity=20, price=200, item_id=44
            ),
            Brand(
                name="Brand 88", min_quantity=5,
                max_quantity=10, price=100, item_id=44
            ),
            Brand(
                name="Brand 89", min_quantity=2,
                max_quantity=20, price=100, item_id=45
            ),
            Brand(
                name="Brand 90", min_quantity=10,
                max_quantity=20, price=300, item_id=45
            ), 
            Brand(
                name="Brand 91", min_quantity=10,
                max_quantity=20, price=200, item_id=46
            ),
            Brand(
                name="Brand 92", min_quantity=10,
                max_quantity=20, price=200, item_id=46
            ),
            Brand(
                name="Brand 93", min_quantity=5,
                max_quantity=10, price=100, item_id=47
            ),
            Brand(
                name="Brand 94", min_quantity=2,
                max_quantity=20, price=100, item_id=47
            ),
            Brand(
                name="Brand 95", min_quantity=10,
                max_quantity=20, price=300, item_id=48
            ),
            Brand(
                name="Brand 96", min_quantity=1,
                max_quantity=10, price=100, item_id=48
            ),
            Brand(
                name="Brand 97", min_quantity=2,
                max_quantity=20, price=100, item_id=49
            ),
            Brand(
                name="Brand 98", min_quantity=10,
                max_quantity=20, price=200, item_id=49
            ),
            Brand(
                name="Brand 99", min_quantity=5,
                max_quantity=10, price=100, item_id=50
            ),
            Brand(
                name="Brand 100", min_quantity=2,
                max_quantity=20, price=100, item_id=50
            ),
            Brand(
                name="Brand 101", min_quantity=10,
                max_quantity=20, price=300, item_id=51
            ),
            Brand(
                name="Brand 102", min_quantity=10,
                max_quantity=20, price=200, item_id=51
            ),
            Brand(
                name="Brand 103", min_quantity=5,
                max_quantity=10, price=100, item_id=52
            ),
            Brand(
                name="Brand 104", min_quantity=2,
                max_quantity=20, price=100, item_id=52
            ),
            Brand(
                name="Brand 105", min_quantity=10,
                max_quantity=20, price=300, item_id=53
            ),
            Brand(
                name="Brand 106", min_quantity=1,
                max_quantity=10, price=100, item_id=53
            ),
            Brand(
                name="Brand 107", min_quantity=2,
                max_quantity=20, price=100, item_id=54
            ),
            Brand(
                name="Brand 108", min_quantity=10,
                max_quantity=20, price=200, item_id=54
            ),
            Brand(
                name="Brand 109", min_quantity=5,
                max_quantity=10, price=100, item_id=55
            ),
            Brand(
                name="Brand 110", min_quantity=2,
                max_quantity=20, price=100, item_id=55
            ),
            Brand(
                name="Brand 111", min_quantity=10,
                max_quantity=20, price=300, item_id=56
            ),
            Brand(
                name="Brand 112", min_quantity=10,
                max_quantity=20, price=200, item_id=56
            ),
            Brand(
                name="Brand 113", min_quantity=5,
                max_quantity=10, price=100, item_id=57
            ),
            Brand(
                name="Brand 114", min_quantity=2,
                max_quantity=20, price=100, item_id=57
            ),
            Brand(
                name="Brand 115", min_quantity=10,
                max_quantity=20, price=300, item_id=58
            ),
            Brand(
                name="Brand 116", min_quantity=1,
                max_quantity=10, price=100, item_id=58
            ),
            Brand(
                name="Brand 117", min_quantity=2,
                max_quantity=20, price=100, item_id=59
            ),
            Brand(
                name="Brand 118", min_quantity=10,
                max_quantity=20, price=200, item_id=59
            ),
            Brand(
                name="Brand 119", min_quantity=5,
                max_quantity=10, price=100, item_id=60
            ),
            Brand(
                name="Brand 120", min_quantity=2,
                max_quantity=20, price=100, item_id=60
            ),
            Brand(
                name="Brand 121", min_quantity=10,
                max_quantity=20, price=300, item_id=61
            ),
            Brand(
                name="Brand 122", min_quantity=10,
                max_quantity=20, price=200, item_id=62
            ),
            Brand(
                name="Brand 123", min_quantity=5,
                max_quantity=10, price=100, item_id=63
            ),
            Brand(
                name="Brand 124", min_quantity=2,
                max_quantity=20, price=100, item_id=64
            ),
            Brand(
                name="Brand 125", min_quantity=10,
                max_quantity=20, price=300, item_id=65
            ),
            Brand(
                name="Brand 126", min_quantity=1,
                max_quantity=10, price=100, item_id=66
            ),
            Brand(
                name="Brand 127", min_quantity=2,
                max_quantity=20, price=100, item_id=67
            ),
            Brand(
                name="Brand 128", min_quantity=10,
                max_quantity=20, price=200, item_id=68
            ),
            Brand(
                name="Brand 129", min_quantity=5,
                max_quantity=10, price=100, item_id=69
            ),
            Brand(
                name="Brand 130", min_quantity=2,
                max_quantity=20, price=100, item_id=70
            ),
            Brand(
                name="Brand 131", min_quantity=10,
                max_quantity=20, price=300, item_id=71
            ),
            Brand(
                name="Brand 132", min_quantity=10,
                max_quantity=20, price=200, item_id=72
            ),
            Brand(
                name="Brand 133", min_quantity=5,
                max_quantity=10, price=100, item_id=73
            ),
            Brand(
                name="Brand 134", min_quantity=2,
                max_quantity=20, price=100, item_id=74
            ),
            Brand(
                name="Brand 135", min_quantity=10,
                max_quantity=20, price=300, item_id=75
            ),
            Brand(
                name="Brand 136", min_quantity=1,
                max_quantity=10, price=100, item_id=76
            ),
            Brand(
                name="Brand 137", min_quantity=2,
                max_quantity=20, price=100, item_id=77
            ),
            Brand(
                name="Brand 138", min_quantity=10,
                max_quantity=20, price=200, item_id=78
            ),
            Brand(
                name="Brand 139", min_quantity=5,
                max_quantity=10, price=100, item_id=79
            ),
            Brand(
                name="Brand 140", min_quantity=2,
                max_quantity=20, price=100, item_id=80
            )
        ]
        Brand.objects.bulk_create(brands_list)
    
    def populate_order_items(self):
        ordered_items_list = [
            OrderItem(
                    user_id=1, item_id=1, brand_id=2, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=2, brand_id=4, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
                OrderItem(
                    user_id=1, item_id=3, brand_id=5, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=4, brand_id=7, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
            OrderItem(
                    user_id=2, item_id=5, brand_id=10, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=3, item_id=6, brand_id=11, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
                OrderItem(
                    user_id=3, item_id=7, brand_id=13, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=3, item_id=8, brand_id=2, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
            ),
            OrderItem(
                    user_id=1, item_id=11, brand_id=21, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=12, brand_id=23, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
                OrderItem(
                    user_id=1, item_id=36, brand_id=71, ordered_quantity=10,
                    delivered_quantity=7, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=42, brand_id=2, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
            OrderItem(
                    user_id=2, item_id=35, brand_id=70, ordered_quantity=10,
                    delivered_quantity=8, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=2, item_id=65, brand_id=125, ordered_quantity=7,
                    delivered_quantity=5, is_out_of_stock=False
                ),
                OrderItem(
                    user_id=3, item_id=27, brand_id=53, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=3, item_id=28, brand_id=56, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
            ),
            OrderItem(
                    user_id=1, item_id=50, brand_id=100, ordered_quantity=10,
                    delivered_quantity=10, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=52, brand_id=103, ordered_quantity=7,
                    delivered_quantity=7, is_out_of_stock=False
                ),
            OrderItem(
                    user_id=1, item_id=31, brand_id=61, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=1, item_id=56, brand_id=111, ordered_quantity=7,
                    delivered_quantity=7, is_out_of_stock=False
                ),
            OrderItem(
                    user_id=2, item_id=23, brand_id=46, ordered_quantity=10,
                    delivered_quantity=10, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=2, item_id=58, brand_id=115, ordered_quantity=7,
                    delivered_quantity=0, is_out_of_stock=False
                ),
                OrderItem(
                    user_id=3, item_id=67, brand_id=127, ordered_quantity=10,
                    delivered_quantity=0, is_out_of_stock=True
                ),
            OrderItem(
                    user_id=3, item_id=38, brand_id=75, ordered_quantity=7,
                    delivered_quantity=7, is_out_of_stock=False
            ),
            OrderItem(
                user_id=2, item_id=40, brand_id=80, ordered_quantity=10,
                delivered_quantity=10, is_out_of_stock=True
            )
        ]
        OrderItem.objects.bulk_create(ordered_items_list)

    def populate_transactions_database(self):
        transactions_list = [
            Transaction(
                payment_transaction_id="12374u3uy34",
                transaction_type=TransactionTypeEnum.PHONE_PAY.value,
                credit_amount=1000.0, screenshot_url="https://google.com",
                remarks="Wallet", user_id=1,
                verification_status=VerificationChoicesEnum.APPROVED.value,
            ),
            Transaction(
                payment_transaction_id=None,
                transaction_type=None,
                debit_amount=100.0, screenshot_url=None,
                remarks="Snacks Form", user_id=1,
                verification_status=None,
            ),
            Transaction(
                payment_transaction_id="12374u3uy34",
                transaction_type=TransactionTypeEnum.PHONE_PAY.value,
                credit_amount=100.0, screenshot_url="https://google.com",
                remarks="Wallet", user_id=1,
                verification_status=VerificationChoicesEnum.PENDING.value,
            ),
            Transaction(
                payment_transaction_id="12374u3uy34",
                transaction_type=TransactionTypeEnum.PHONE_PAY.value,
                credit_amount=9000.0, screenshot_url="https://google.com",
                remarks="Health Kit", user_id=1,
                verification_status=VerificationChoicesEnum.DECLINED.value,
            ),
            Transaction(
                payment_transaction_id="12374u3uy34",
                transaction_type=TransactionTypeEnum.PHONE_PAY.value,
                credit_amount=1000.0, screenshot_url="https://google.com",
                remarks="Wallet", user_id=2,
                verification_status=VerificationChoicesEnum.PENDING.value,
            ),
            Transaction(
                payment_transaction_id=None,
                transaction_type=None,
                debit_amount=100.0, screenshot_url=None,
                remarks="Acco Form", user_id=3,
                verification_status=None,
            ),
            Transaction(
                payment_transaction_id="12374u3uy34",
                transaction_type=TransactionTypeEnum.PHONE_PAY.value,
                credit_amount=1000.0, screenshot_url="https://google.com",
                remarks="Wallet", user_id=3,
                verification_status=VerificationChoicesEnum.APPROVED.value,
            ),
            Transaction(
                payment_transaction_id=None,
                transaction_type=None,
                debit_amount=100.0, screenshot_url=None,
                remarks="Health Kit", user_id=3,
                verification_status=None,
            )
        ]
        Transaction.objects.bulk_create(transactions_list)

    def populate_bank_details_database(self):
        BankDetails.objects.create(upi_id="8247088772@SBI")
 
 
def populate_database():
    populate = PopulateDatabase()
    #populate.populate_user_database()
    populate.populate_forms_database()
    populate.populate_section_database()
    populate.populate_item_database()
    populate.populate_brand_database()
    populate.populate_order_items()
    #populate.populate_wallet_database()
    populate.populate_transactions_database()
    populate.populate_bank_details_database()
