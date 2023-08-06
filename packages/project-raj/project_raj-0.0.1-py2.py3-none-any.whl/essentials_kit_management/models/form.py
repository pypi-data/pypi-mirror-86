from django.db import models
from essentials_kit_management.models import User
from essentials_kit_management.constants.enums import StatusEnum


class Form(models.Model):
    status_choices = [
        (status.value, status.value)
        for status in StatusEnum
    ]

    description = models.TextField()
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50, choices=status_choices, null=True, blank=True,
        default=StatusEnum.LIVE.value
    )
    close_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name="forms")
