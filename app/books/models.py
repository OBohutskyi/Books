from django.db import models
from datetime import datetime
from app.users.models import User


class Book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def obj(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'creator': self.creator.obj()}

    def __str__(self):
        return 'id: ' + str(self.id) + ', name:' + str(self.name) + ', description:' + str(self.description)
