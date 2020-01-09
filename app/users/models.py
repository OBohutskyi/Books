from django.db import models
import hashlib

# Create your models here.
class User:
    ID = 0

    def __init__(self, username, password):
        User.ID += 1
        self.id = User.ID
        self.username = username
        self.password_hash = self.get_hash(password)

    def obj(self):
        return {'id': str(self.id), 'username': self.username}

    def get_hash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        return self.username == other.username
