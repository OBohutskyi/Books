from datetime import datetime, timedelta
import hashlib
import jwt
from django.db import models

key = 'secret'


class User(models.Model):
    username = models.CharField(max_length=30)
    password_hash = models.TextField(max_length=64)

    def obj(self):
        return {'id': str(self.id), 'username': self.username}

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return self.id

    def create_user_token(self):
        return jwt.encode({'username': self.username,
                           'exp': (datetime.now() + timedelta(days=1)).timestamp()},
                          key, algorithm='HS256').decode()

    @staticmethod
    def get_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
