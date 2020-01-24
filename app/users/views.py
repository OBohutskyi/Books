from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import AuthenticationFailed
from app.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from app.auth import UserAuthentication, UsersViewAuthentication


class UsersView(ViewSet):
    authentication_classes = (UsersViewAuthentication,)

    def get(self, request):
        all_users = list(User.objects.all())
        return JsonResponse({'users': [b.obj() for b in all_users]})

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            is_user_present = User.objects.filter(username=username)
            if len(is_user_present):
                return JsonResponse({'message': 'User with such username already exists'}, status=409)
            new_user = User.objects.create(username=username, password_hash=User.get_hash(password))
            return JsonResponse({'message': 'Successfully created user, id: ' + str(new_user.id)}, status=201)
        return JsonResponse({'message': 'Invalid data'}, status=400)


class SingleUserView(ViewSet):
    authentication_classes = (UserAuthentication,)

    def get(self, request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({'user': user.obj()})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'User doesn\'t exist'}, status=401)

    def update(self, request, user_id: int):
        new_password = request.data.get('password')
        if new_password:
            existing_user = User.objects.filter(id=user_id)
            if not existing_user:
                return JsonResponse({'message': 'User doesn\'t exist'}, status=401)
            existing_user.update(password_hash=User.get_hash(new_password))
            return JsonResponse({'message': 'Successfully updated user'})
        return JsonResponse({'message': 'Invalid data'}, status=400)

    def delete(self, request, user_id):
        try:
            removed_user = User.objects.get(id=user_id)
            User.objects.filter(id=user_id).delete()
            response_message = {'message': 'removed user'}
            response_message['user'] = removed_user.obj()
            return JsonResponse(response_message)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=409)


class UserLogin(ViewSet):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.password_hash == User.get_hash(password):
                    return JsonResponse({'access_token': User.create_user_token(user)}, status=201)
                else:
                    raise AuthenticationFailed('Password is incorrect')
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'User wasn\'t found'}, status=401)
        return JsonResponse({'message': 'Invalid data'}, status=400)
