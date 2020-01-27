import mock
from app.users.models import User


class UserMock:

    def __init__(self):
        self.objects = UserMock.UserMockObjects()

    class UserMockObjects:

        def __init__(self):
            test_user = User(username='test', password_hash='test_hash')
            self.all = mock.Mock(return_value=[test_user])
            self.create = mock.Mock(return_value=test_user)
            self.get = mock.Mock(return_value=test_user)
            self.filter = mock.Mock(return_value=NonEmptyFilterMock(test_user))


class NonEmptyFilterMock:

    def __init__(self, test_user):
        self.return_value = mock.Mock(return_value=iter([test_user]))
        self.delete = mock.Mock(return_value=(1, {'users.User': 1}))
        self.update = mock.Mock(return_value=[test_user])

    def __len__(self):
        return 1


class EmptyFilterMock:

    def __len__(self):
        return 0


class MockUserAuthentication:

    def authenticate(self, request):
        request.META['HTTP_CUSTOM_HEADER'] = [1]
        return 'decoded_token', None
