import mock
from django.db.models.query import QuerySet
from app.books.models import Book


class BookMock:

    def __init__(self):
        self.objects = BookMock.BookMockObjects()

    class BookMockObjects:

        def __init__(self):
            test_book = Book(name='test book')
            test_book.id = 1
            test_book.obj = mock.Mock(return_value={'id': 'None', 'name': 'test book', 'description': ''})
            self.all = mock.Mock(return_value=[test_book])
            self.create = mock.Mock(return_value=test_book)
            self.get = mock.Mock(return_value=test_book)
            self.filter = mock.Mock(return_value=FilterMock(test_book))


class FilterMock:

    def __init__(self, test_book):
        self.return_value = mock.Mock(return_value=iter([test_book]))
        self.delete = mock.Mock(return_value=(1, {'books.Book': 1}))

    class QueryMock(QuerySet):

        def __init__(self):
            super().__init__()
