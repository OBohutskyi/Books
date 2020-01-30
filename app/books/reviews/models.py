from django.db import models
from app.books.models import Book
from app.users.models import User


class Review(models.Model):
    review = models.TextField(max_length=500)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def obj(self):
        return {
            'id': str(self.id),
            'book_id': self.book_id_id,
            'reviewed_by': self.reviewed_by_id,
            'review': self.review
        }
