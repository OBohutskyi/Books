import pytest
import jwt
import mock
from app.auth import UserAuthentication
from rest_framework.test import APIRequestFactory
import app.auth
from rest_framework import exceptions


class TestUserAuthentication:

    def setup(self) -> None:
        self.factory = APIRequestFactory()

    def test_authenticate_without_token(self):
        request = self.factory.post('/users/',
                                    {},
                                    HTTP_AUTHORIZATION='Bearer')

        with pytest.raises(exceptions.AuthenticationFailed) as e:
            UserAuthentication().authenticate(request)

        assert 'Invalid token header. No credentials provided.' == str(e.value)

    def test_authenticate_too_many_token_words(self):
        request = self.factory.post('/users/',
                                    {},
                                    HTTP_AUTHORIZATION='Bearer 1 2')

        with pytest.raises(exceptions.AuthenticationFailed) as e:
            UserAuthentication().authenticate(request)

        assert 'Invalid token header. Token string should not contain spaces.' == str(e.value)

    def test_authenticate_valid_token(self):
        decoded_token = {'username': 'test username',
                         'books_ids': [1]}
        jwt.decode = mock.Mock(return_value=decoded_token)
        request = self.factory.post('/users/',
                                    {},
                                    HTTP_AUTHORIZATION='Bearer {}'.format('test_token'))

        result = UserAuthentication().authenticate(request)

        assert decoded_token, None == result
        assert request.META['HTTP_CUSTOM_HEADER'] == [1]
        jwt.decode.assert_called_with('test_token', app.auth.key, algorithm='HS256')

    def test_authenticate_expired_token(self):
        jwt.decode = mock.Mock(side_effect=jwt.ExpiredSignatureError())
        request = self.factory.post('/users/',
                                    {},
                                    HTTP_AUTHORIZATION='Bearer {}'.format('test_token'))

        with pytest.raises(exceptions.AuthenticationFailed) as e:
            UserAuthentication().authenticate(request)

        assert 'Token was expired' == str(e.value)
        jwt.decode.assert_called_with('test_token', app.auth.key, algorithm='HS256')

    def test_authenticate_invalid_token(self):
        jwt.decode = mock.Mock(side_effect=jwt.DecodeError())
        request = self.factory.post('/users/',
                                    {},
                                    HTTP_AUTHORIZATION='Bearer {}'.format('test_token'))

        with pytest.raises(exceptions.AuthenticationFailed) as e:
            UserAuthentication().authenticate(request)

        assert 'Invalid token header.' == str(e.value)
        jwt.decode.assert_called_with('test_token', app.auth.key, algorithm='HS256')
