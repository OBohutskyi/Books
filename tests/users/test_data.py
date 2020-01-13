import pytest
import mock
from app.users.data import UsersData
from app.users.models import User


class TestUsersData:

    def setup(self) -> None:
        self.users_data = UsersData()

    def setup_class(cls):
        cls.user = User('new_user', 'password')

    @mock.patch('app.users.data.registered_users')
    def test_add_new_user(self, mock_registered_users):
        mock_registered_users.append = mock.Mock()

        result = self.users_data.add(self.user)

        assert True is result
        mock_registered_users.append.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_add_existing_user(self, mock_registered_users):
        mock_registered_users.append = mock.Mock()
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.add(self.user)

        assert False is result
        mock_registered_users.append.assert_not_called()

    @mock.patch('app.users.data.registered_users')
    def test_delete_existing_user(self, mock_registered_users):
        mock_registered_users.remove = mock.Mock()
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.delete(str(self.user.id))

        assert self.user == result
        mock_registered_users.remove.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_delete_not_existing_user(self, mock_registered_users):
        mock_registered_users.remove = mock.Mock(side_effect=ValueError)

        with pytest.raises(Exception) as e:
            self.users_data.delete(self.user.username)

        assert 'User not found' == str(e.value)

    @mock.patch('app.users.data.registered_users')
    def test_update_existing_user(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.update(str(self.user.id), 'new_password_hash')

        assert True is result

    @mock.patch('app.users.data.registered_users')
    def test_update_not_existing_user(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([]))

        result = self.users_data.update(2, 'new_password_hash')

        assert False is result

    def test_get_without_parameters_returns_registered_users(self):
        result = self.users_data.get()

        assert [] == result

    @mock.patch('app.users.data.registered_users')
    def test_get_with_valid_id_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id=str(1))

        assert [self.user] == result

    @mock.patch('app.users.data.registered_users')
    def test_get_with_not_valid_id_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id=2)

        assert [] == result

    @mock.patch('app.users.data.registered_users')
    def test_get_with_invalid_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id_d=2)

        assert [self.user] == result

    @mock.patch('app.users.data.registered_users')
    def test_is_user_present_returns_user(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.is_user_present(self.user.username)

        assert self.user == result

    @mock.patch('app.users.data.registered_users')
    def test_is_user_present_returns_false(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([]))

        result = self.users_data.is_user_present(self.user.username)

        assert False is result
