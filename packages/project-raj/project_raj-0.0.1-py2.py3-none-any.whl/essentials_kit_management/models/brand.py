from django.db import models
from essentials_kit_management.models.item import Item


class Brand(models.Model):
    name = models.CharField(max_length=100)
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    price = models.FloatField()
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="brands"
    )
