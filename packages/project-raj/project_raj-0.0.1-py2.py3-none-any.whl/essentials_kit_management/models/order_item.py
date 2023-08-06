from django.db import models
from essentials_kit_management.models import User
from essentials_kit_management.models.item import Item
from essentials_kit_management.models.brand import Brand


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_ordered_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="ordered_items"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="ordered_items_brands"
    )
    ordered_quantity = models.IntegerField()
    delivered_quantity = models.IntegerField(default=0)
    is_out_of_stock = models.BooleanField(default=False)
