from django.db import models


class BankDetails(models.Model):
    upi_id = models.CharField(max_length=100)
