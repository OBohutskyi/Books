from django.test import Client
from django.urls import reverse
from app.users.data import User
import mock


class TestUsersView:

    def setup_class(cls):
        cls.user = User('new_user', 'password')

    def test_get_when_users_arent_created_returns_empty_list(self):
        resp = Client().get(reverse('users_list'))

        assert {'users': []} == resp.json()

    @mock.patch('app.users.views.users_data')
    def test_get_returns_all_users(self, mock_users_data):
        self.user.obj = mock.Mock(return_value={'id': 1, 'username': 'user'})
        mock_users_data.get = mock.Mock(return_value=iter([self.user]))

        resp = Client().get(reverse('users_list'))

        assert {'users': [{'id': 1, 'username': 'user'}]} == resp.json()
        mock_users_data.get.assert_called()
        self.user.obj.assert_called()

    @mock.patch('app.users.views.users_data')
    def test_post_new_user(self, mock_users_data):
        mock_users_data.add = mock.Mock(return_value=True)

        resp = Client().post(reverse('users_list'), {'username': 'username', 'password': 'password'})

        assert {'message': 'Successfully created user'} == resp.json()
        assert 201 == resp.status_code
        mock_users_data.add.assert_called()

    @mock.patch('app.users.views.users_data')
    def test_post_existing_user(self, mock_users_data):
        mock_users_data.add = mock.Mock(return_value=False)

        resp = Client().post(reverse('users_list'), {'username': 'username', 'password': 'password'})

        assert {'message': 'User with such username already exists'} == resp.json()
        assert 409 == resp.status_code
        mock_users_data.add.assert_called()

    def test_post_not_valid_body_data(self):
        resp = Client().post(reverse('users_list'), {'test': 'test_data'})

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code


class TestSingleUserView:

    def setup_class(cls):
        cls.user = User('new_user', 'password')

    @mock.patch('app.users.views.users_data')
    def test_get_valid_user_id(self, mock_users_data):
        mock_users_data.get = mock.Mock(return_value=iter([self.user]))

        resp = Client().get(reverse('user', args=[1]))

        assert {'user': [{'id': str(self.user.id), 'username': self.user.username}]} == resp.json()
        mock_users_data.get.assert_called_with(id='1')

    @mock.patch('app.users.views.users_data')
    def test_get_not_valid_user_id(self, mock_users_data):
        mock_users_data.get = mock.Mock(return_value=[])

        resp = Client().get(reverse('user', args=[1]))

        assert {'message': 'User wasn\'t found'} == resp.json()
        mock_users_data.get.assert_called_with(id='1')

    @mock.patch('app.users.views.users_data')
    def test_update_existing_user(self, mock_users_data):
        mock_users_data.update = mock.Mock(return_value=True)

        resp = Client().put(
            reverse('user', args=[1]),
            {'password': 'new_password'},
            content_type='application/json')

        assert {'message': 'Successfully updated user'} == resp.json()
        mock_users_data.update.assert_called()

    @mock.patch('app.users.views.users_data')
    def test_update_not_existing_user(self, mock_users_data):
        mock_users_data.update = mock.Mock(return_value=False)

        resp = Client().put(
            reverse('user', args=[1]),
            {'password': 'new_password'},
            content_type='application/json')

        assert {'message': 'Unable update user'} == resp.json()
        mock_users_data.update.assert_called()

    def test_update_invalid_data(self):
        resp = Client().put(
            reverse('user', args=[1]),
            {'test': 'test_data'},
            content_type='application/json')

        assert {'message': 'Invalid data'} == resp.json()

    @mock.patch('app.users.views.users_data')
    def test_delete_existing_user(self, mock_users_data):
        mock_users_data.delete = mock.Mock(return_value=self.user)

        resp = Client().delete(reverse('user', args=[str(self.user.id)]))

        assert {'message': 'Removed user: ' + self.user.username} == resp.json()
        assert 200 == resp.status_code
        mock_users_data.delete.assert_called_with(str(self.user.id))

    @mock.patch('app.users.views.users_data')
    def test_delete_not_existing_user(self, mock_users_data):
        mock_users_data.delete = mock.Mock(side_effect=Exception('User not found'))

        resp = Client().delete(reverse('user', args=[str(self.user.id)]))

        assert {'message': 'User not found'} == resp.json()
        assert 409 == resp.status_code
        mock_users_data.delete.assert_called_with(str(self.user.id))


class TestUserLogin:

    def setup_class(cls):
        cls.user = User('new_user', 'password')

    @mock.patch('app.users.views.User.create_user_token', return_value='test_token')
    @mock.patch('app.users.views.users_data')
    @mock.patch('app.users.views.User')
    def test_post_valid_username_and_password(self, mock_user, users_data, mock_create_user_token):
        mock_user.get_hash = mock.Mock(return_value=self.user.password_hash)
        users_data.is_user_present = mock.Mock(return_value=self.user)

        resp = Client().post(reverse('login'), {'username': self.user.username, 'password': 'password'})

        assert {'access_token': 'test_token'} == resp.json()
        users_data.is_user_present.assert_called_with(self.user.username)
        mock_user.get_hash.assert_called_with('password')
        mock_create_user_token.assert_called()

    @mock.patch('app.users.views.users_data')
    @mock.patch('app.users.views.User')
    def test_post_valid_username_not_valid_password(self, mock_user, users_data):
        mock_user.get_hash = mock.Mock(return_value='')
        users_data.is_user_present = mock.Mock(return_value=self.user)

        resp = Client().post(reverse('login'), {'username': self.user.username, 'password': 'password'})

        assert {'detail': 'Password is incorrect'} == resp.json()
        users_data.is_user_present.assert_called_with(self.user.username)
        mock_user.get_hash.assert_called_with('password')

    @mock.patch('app.users.views.users_data')
    def test_post_not_valid_username(self, users_data):
        users_data.is_user_present = mock.Mock(return_value=False)

        resp = Client().post(reverse('login'), {'username': self.user.username, 'password': 'password'})

        assert {'message': 'User wasn\'t found'} == resp.json()
        assert 401 == resp.status_code
        users_data.is_user_present.assert_called_with(self.user.username)

    def test_post_invalid_data(self):
        resp = Client().post(reverse('login'), {'test': 'test'})

        assert {'message': 'Invalid data'} == resp.json()
        assert 400 == resp.status_code
