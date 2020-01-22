from rest_framework import authentication
from rest_framework import exceptions
import jwt

key = 'secret'


class UserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'bearer' or len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
            decoded_token = jwt.decode(token, key, algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token was expired')
        except (jwt.DecodeError, UnicodeError):
            raise exceptions.AuthenticationFailed('Invalid token header.')

        return decoded_token, None
