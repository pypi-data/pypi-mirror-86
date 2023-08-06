from django.db import models
from essentials_kit_management.models import User
from essentials_kit_management.constants.enums \
    import TransactionTypeEnum, VerificationChoicesEnum

class Transaction(models.Model):
    transaction_choices = [
        (transaction_type.value, transaction_type.value)
        for transaction_type in TransactionTypeEnum
    ]
    verification_choices = [
        (verification_choice.value, verification_choice.value)
        for verification_choice in VerificationChoicesEnum
    ]

    payment_transaction_id = models.CharField(
        max_length=100, null=True, blank=True
    )
    transaction_type = models.CharField(
        max_length=50, choices=transaction_choices, blank=True, null=True
    )
    credit_amount = models.FloatField(default=0)
    debit_amount = models.FloatField(default=0)
    transaction_date = models.DateTimeField(auto_now=True)
    screenshot_url = models.URLField(null=True, blank=True)
    remarks = models.CharField(max_length=100)
    verification_status = models.CharField(
        max_length=50, choices=verification_choices, blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_transaction"
    )
