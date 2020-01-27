from django.test import Client
from django.urls import reverse
from mock import PropertyMock, patch
from .mocks import UserMock, EmptyFilterMock, MockUserAuthentication
import mock
from django.core.exceptions import ObjectDoesNotExist
from app.auth import UserAuthentication


class TestUsersView:

    def setup(self) -> None:
        self.user_mock = UserMock()

    def test_get_when_users_arent_created_returns_empty_list(self):
        UserAuthentication.authenticate = MockUserAuthentication.authenticate
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().get(reverse('users_list'))

            assert {'users': [{'id': 'None', 'username': 'test'}]} == resp.json()
            assert 200 == resp.status_code
            self.user_mock.objects.all.assert_called()

    def test_post_new_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects
            self.user_mock.objects.filter = mock.Mock(return_value=EmptyFilterMock())

            resp = Client().post(reverse('users_list'), {'username': 'test username', 'password': 'test password'})

            assert {'message': 'Successfully created user, id: None'} == resp.json()
            assert 201 == resp.status_code
            self.user_mock.objects.create.assert_called()

    def test_post_existing_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().post(reverse('users_list'), {'username': 'test username', 'password': 'test password'})

            assert {'message': 'User with such username already exists'} == resp.json()
            assert 409 == resp.status_code

    def test_post_with_invalid_data(self):
        resp = Client().post(reverse('users_list'), {'test': 'test data'})

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code


class TestSingleUserView:

    def setup(self) -> None:
        self.user_mock = UserMock()
        UserAuthentication.authenticate = MockUserAuthentication.authenticate

    def test_get_valid_user_id(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().get(reverse('user', args=[1]))

            assert {'user': {'id': 'None', 'username': 'test'}} == resp.json()
            assert 200 == resp.status_code
            self.user_mock.objects.get.assert_called_with(id='1')

    def test_get_not_valid_user_id(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects
            self.user_mock.objects.get = mock.Mock(side_effect=ObjectDoesNotExist)

            resp = Client().get(reverse('user', args=[1]))

            assert {'message': "User doesn't exist"} == resp.json()
            assert 401 == resp.status_code
            self.user_mock.objects.get.assert_called_with(id='1')

    def test_update_existing_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().put(
                reverse('user', args=[1]),
                {'password': 'updated_password'},
                content_type='application/json')

            assert {'message': 'Successfully updated user'} == resp.json()
            assert 200 == resp.status_code
            self.user_mock.objects.filter.assert_called_with(id='1')
            self.user_mock.objects.filter().update.assert_called()

    def test_update_not_existing_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects
            self.user_mock.objects.filter = mock.Mock(return_value=EmptyFilterMock())

            resp = Client().put(
                reverse('user', args=[1]),
                {'password': 'updated_password'},
                content_type='application/json')

            assert {'message': "User doesn't exist"} == resp.json()
            assert 401 == resp.status_code
            self.user_mock.objects.filter.assert_called_with(id='1')

    def test_update_invalid_data(self):
        resp = Client().put(
                reverse('user', args=[1]),
                {'test': 'test_data'},
                content_type='application/json')

        assert {'message': 'Invalid data'} == resp.json()

    def test_delete_existing_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().delete(reverse('user', args=[1]))

            assert {'message': 'removed user', 'user': {'id': 'None', 'username': 'test'}} == resp.json()
            assert 200 == resp.status_code
            self.user_mock.objects.get.assert_called_with(id='1')
            self.user_mock.objects.filter.assert_called_with(id='1')

    def test_delete_not_existing_user(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects
            self.user_mock.objects.get = mock.Mock(side_effect=ObjectDoesNotExist('Test Exception'))

            resp = Client().delete(reverse('user', args=[1]))

            assert {'message': 'Test Exception'} == resp.json()
            assert 409 == resp.status_code
            self.user_mock.objects.get.assert_called_with(id='1')


class TestUserLogin:

    def setup(self) -> None:
        self.user_mock = UserMock()

    @mock.patch('app.users.views.User.get_hash', return_value='test_hash')
    @mock.patch('app.users.views.User.create_user_token', return_value='test_token')
    def test_post_valid_username_and_password(self, mock_create_user_token, mock_get_hash):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().post(reverse('login'), {'username': 'username', 'password': 'password'})

            assert {'access_token': 'test_token'} == resp.json()
            assert 201 == resp.status_code
            self.user_mock.objects.get.assert_called_with(username='username')
            mock_create_user_token.assert_called_with(self.user_mock.objects.get.return_value)
            mock_get_hash.assert_called_with('password')

    @mock.patch('app.users.views.User.get_hash', return_value='test_incorrect_hash')
    def test_post_valid_username_not_valid_password(self, mock_get_hash):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects

            resp = Client().post(reverse('login'), {'username': 'username', 'password': 'password'})

            assert {'detail': 'Password is incorrect'} == resp.json()
            assert 403 == resp.status_code
            self.user_mock.objects.get.assert_called_with(username='username')
            mock_get_hash.assert_called_with('password')

    def test_post_not_valid_username(self):
        with patch('app.users.views.User.objects', new_callable=PropertyMock) as mock_users_objects:
            mock_users_objects.return_value = self.user_mock.objects
            self.user_mock.objects.get = mock.Mock(side_effect=ObjectDoesNotExist('Test Exception'))

            resp = Client().post(reverse('login'), {'username': 'username', 'password': 'password'})

            assert {'message': "User wasn't found"} == resp.json()
            assert 401 == resp.status_code
            self.user_mock.objects.get.assert_called_with(username='username')

    def test_post_invalid_data(self):
        resp = Client().post(reverse('login'), {'test': 'test'})

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code
