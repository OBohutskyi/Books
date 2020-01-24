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
        from app.books.models import Book
        # print(User.objects.get(id=1).books)
        books = Book.objects.filter(creator_id=self.id)
        books_ids = [x.id for x in books]
        return jwt.encode({'username': self.username,
                           'books_ids': books_ids,
                           'exp': (datetime.now() + timedelta(days=1)).timestamp()},
                          key, algorithm='HS256').decode()

    @staticmethod
    def get_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
