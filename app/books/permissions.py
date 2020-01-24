from rest_framework.exceptions import AuthenticationFailed


def book_write_permission(f):

    def check_permission(self, request, book_id):
        if int(book_id) in request.META['HTTP_CUSTOM_HEADER']:
            return f(self, request, book_id)
        else:
            raise AuthenticationFailed()

    return check_permission

