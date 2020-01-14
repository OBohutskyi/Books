import mock

from app.books.models import Book


class BookMock:

    def __init__(self):
        self.objects = BookMock.BookMockObjects()

    class BookMockObjects:

        def __init__(self):
            test_book = Book(name='test book')
            test_book.obj = mock.Mock(return_value={'id': 'None', 'name': 'test book', 'description': ''})
            self.all = mock.Mock(return_value=[test_book])
