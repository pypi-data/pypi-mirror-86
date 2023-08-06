from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from essentials_kit_management.models import User, Form, Brand, \
    OrderItem, Section, Item, Transaction, BankDetails


admin.site.register(User, UserAdmin)
admin.site.register(Form)
admin.site.register(Brand)
admin.site.register(OrderItem)
admin.site.register(Section)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(BankDetails)
