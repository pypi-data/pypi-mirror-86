from django.db import models
from essentials_kit_management.models.form import Form


class Section(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="sections"
    )
