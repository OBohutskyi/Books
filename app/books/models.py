from django.db import models
from datetime import datetime


class Book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(default=datetime.now)
