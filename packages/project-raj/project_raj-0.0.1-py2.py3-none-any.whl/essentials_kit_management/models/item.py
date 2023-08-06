from django.db import models
from essentials_kit_management.models.section import Section


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="items"
    )
