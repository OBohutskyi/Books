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

        assert result is True
        mock_registered_users.append.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_add_existing_user(self, mock_registered_users):
        mock_registered_users.append = mock.Mock()
        mock_registered_users.__contains__ = mock.Mock(return_value=True)

        result = self.users_data.add(self.user)

        assert result is False
        mock_registered_users.append.assert_not_called()
        mock_registered_users.__contains__.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_delete_existing_user(self, mock_registered_users):
        mock_registered_users.remove = mock.Mock()

        result = self.users_data.delete(self.user)

        assert result == self.user
        mock_registered_users.remove.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_delete_not_existing_user(self, mock_registered_users):
        mock_registered_users.remove = mock.Mock(side_effect=ValueError)

        with pytest.raises(Exception) as e:
            self.users_data.delete(self.user)

        assert str(e.value) == 'User not found'
        mock_registered_users.remove.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_update_existing_user(self, mock_registered_users):
        mock_registered_users.index = mock.Mock()

        result = self.users_data.update(self.user, 'new_password_hash')

        assert result is True
        mock_registered_users.index.assert_called_with(self.user)

    @mock.patch('app.users.data.registered_users')
    def test_update_not_existing_user(self, mock_registered_users):
        mock_registered_users.index = mock.Mock(side_effect=ValueError)

        new_user = User('new_user2', 'password2')
        result = self.users_data.update(new_user, 'new_password_hash')

        assert result is False
        mock_registered_users.index.assert_called_with(new_user)

    def test_get_without_parameters_returns_registered_users(self):
        result = self.users_data.get()

        assert result == []

    @mock.patch('app.users.data.registered_users')
    def test_get_with_valid_id_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id=1)

        assert result == [self.user]

    @mock.patch('app.users.data.registered_users')
    def test_get_with_not_valid_id_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id=2)

        assert result == []

    @mock.patch('app.users.data.registered_users')
    def test_get_with_invalid_parameter(self, mock_registered_users):
        mock_registered_users.__iter__ = mock.Mock(return_value=iter([self.user]))

        result = self.users_data.get(id_d=2)

        assert result == [self.user]
