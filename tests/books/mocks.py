import mock
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
        self.test_book = test_book
        self.return_value = mock.Mock(return_value=iter([test_book]))
        self.delete = mock.Mock(return_value=(1, {'books.Book': 1}))
        self.update = mock.Mock(return_value=[test_book])

    def __getitem__(self, indices):
        return self.test_book


class MockUserAuthentication:

    def authenticate(self, request):
        request.META['HTTP_CUSTOM_HEADER'] = [1]
        return 'decoded_token', None
