# from django.db import models
from datetime import datetime, timedelta
import hashlib
import jwt


class User:
    ID = 0

    def __init__(self, username, password):
        User.ID += 1
        self.id = User.ID
        self.username = username
        self.password_hash = self.get_hash(password)

    def obj(self):
        return {'id': str(self.id), 'username': self.username}

    def __eq__(self, other):
        return self.username == other.username

    @staticmethod
    def create_user_token(user):
        return jwt.encode({'username': user.username, 'exp': (datetime.now() + timedelta(seconds=5)).timestamp()},
                          user.password_hash, algorithm='HS256').decode()

    @staticmethod
    def get_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
