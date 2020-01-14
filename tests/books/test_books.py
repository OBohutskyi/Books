from django.test import Client
from django.urls import reverse
from mock import PropertyMock, patch
from .mocks import BookMock
from app.books.models import Book


class TestBooksView:

    def setup_class(cls):
        cls.book = Book(name='test_book', description='book for testing')

    def test_get(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = BookMock().objects

            resp = Client().get(reverse('books_list'))

            assert {'books': [{'description': '', 'id': 'None', 'name': 'test book'}]} == resp.json()
            assert 200 == resp.status_code
            mock_books_objects.all.assert_called()
