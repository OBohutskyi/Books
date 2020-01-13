from django.http import JsonResponse, HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import AuthenticationFailed
from app.users.data import UsersData
from app.users.models import User

users_data = UsersData()


class UsersView(ViewSet):

    def get(self, request):
        return JsonResponse({'users': [i.obj() for i in users_data.get()]})

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            if users_data.add(User(username, password)):
                return JsonResponse({'message': 'Successfully created user'}, status=201)
            else:
                return JsonResponse({'message': 'User with such username already exists'}, status=409)
        return JsonResponse({'message': 'Invalid data'}, status=400)


class SingleUserView(ViewSet):
    def get(self, request, user_id: int):
        result = users_data.get(id=user_id)
        if result:
            return JsonResponse({'user': [x.obj() for x in result]})
        return JsonResponse({'message': 'User wasn\'t found'})

    def update(self, request, user_id: int):
        new_password = request.data.get('password')
        if new_password:
            if users_data.update(user_id, User.get_hash(new_password)):
                return JsonResponse({'message': 'Successfully updated user'})
            else:
                return JsonResponse({'message': 'Unable update user'}, status=409)
        return JsonResponse({'message': 'Invalid data'}, status=400)

    def delete(self, request, user_id):
        try:
            removed_user = users_data.delete(user_id)
            return JsonResponse({'message': 'Removed user: ' + removed_user.username})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=409)


class UserLogin(ViewSet):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = users_data.is_user_present(username)
            if user:
                if User.get_hash(password) == user.password_hash:
                    return JsonResponse({'access_token': User.create_user_token(user)}, status=201)
                else:
                    # return JsonResponse({'message': 'Password is incorrect'}, status=401)
                    raise AuthenticationFailed('Password is incorrect')
            else:
                return JsonResponse({'message': 'User wasn\'t found'}, status=401)
        return JsonResponse({'message': 'Invalid data'}, status=400)
