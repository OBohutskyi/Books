from django.test import Client
from django.urls import reverse
from mock import PropertyMock, patch
from .mocks import BookMock
import mock
from django.core.exceptions import ObjectDoesNotExist


class TestBooksView:

    def setup(self) -> None:
        self.book_mock = BookMock()

    def test_get(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects

            resp = Client().get(reverse('books_list'))

            assert {'books': [{'description': '', 'id': 'None', 'name': 'test book'}]} == resp.json()
            assert 200 == resp.status_code
            self.book_mock.objects.all.assert_called()

    def test_post(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects

            resp = Client().post(reverse('books_list'), {'name': 'test name', 'description': 'test description'})

            assert {'message': 'Successfully created book, id: 1'} == resp.json()
            assert 201 == resp.status_code
            self.book_mock.objects.create.assert_called()

    def test_post_with_invalid_data(self):
        resp = Client().post(reverse('books_list'), {'test': 'test data'})

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code


class TestSingleBookView:

    def setup(self) -> None:
        self.book_mock = BookMock()

    def test_get_valid_book_id(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects

            resp = Client().get(reverse('book', args=[1]))

            assert {'book': {'id': 'None', 'name': 'test book', 'description': ''}} == resp.json()
            assert 200 == resp.status_code
            self.book_mock.objects.get.assert_called_with(id='1')

    def test_get_with_invalid_data(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects
            self.book_mock.objects.get = mock.Mock(side_effect=ObjectDoesNotExist)

            resp = Client().get(reverse('book', args=[1]))

            assert {'message': 'Book doesn\'t exist'} == resp.json()
            assert 401 == resp.status_code
            self.book_mock.objects.get.assert_called_with(id='1')

    def test_delete(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects

            resp = Client().delete(reverse('book', args=[1]))

            assert {'message': 'removed book', 'book': {'id': 'None', 'name': 'test book', 'description': ''}} == \
                   resp.json()
            assert 200 == resp.status_code
            self.book_mock.objects.get.assert_called_with(id='1')
            self.book_mock.objects.filter.assert_called_with(id='1')
            self.book_mock.objects.filter().delete.assert_called()

    def test_delete_book_do_not_exists(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects
            self.book_mock.objects.get = mock.Mock(side_effect=ObjectDoesNotExist)

            resp = Client().delete(reverse('book', args=[1]))

            assert {'message': 'Book doesn\'t exist'} == resp.json()
            assert 401 == resp.status_code
            self.book_mock.objects.get.assert_called_with(id='1')

    def test_update(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects

            resp = Client().put(
                reverse('book', args=[1]),
                {'name': 'updated_name', 'description': 'updated_description'},
                content_type='application/json')

            assert {'message': 'Successfully updated book', 'book': {'id': 'None', 'name': 'test book',
                                                                     'description': ''}} == resp.json()
            assert 200 == resp.status_code
            self.book_mock.objects.filter.assert_called_with(id='1')
            self.book_mock.objects.filter().update.assert_called()

    def test_update_book_do_not_exists(self):
        with patch('app.books.views.Book.objects', new_callable=PropertyMock) as mock_books_objects:
            mock_books_objects.return_value = self.book_mock.objects
            self.book_mock.objects.filter = mock.Mock(side_effect=ObjectDoesNotExist)

            resp = Client().put(
                reverse('book', args=[1]),
                {'name': 'updated_name'},
                content_type='application/json')

            assert {'message': "Book doesn't exist"} == resp.json()
            assert 401 == resp.status_code
            self.book_mock.objects.filter.assert_called_with(id='1')

    def test_update_invalid_data(self):
        resp = Client().put(reverse('book', args=[1]))

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code
