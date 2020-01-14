from django.db import models
from datetime import datetime


class Book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(default=datetime.now)

    def obj(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

    def __str__(self):
        return self.name

