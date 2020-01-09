from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from rest_framework.viewsets import ViewSet
import json
import jwt
import hashlib

registered_users = []


class User:
    ID = 0

    def __init__(self, username, password):
        User.ID += 1
        self.id = User.ID
        self.username = username
        self.password_hash = get_hash(password)

    # def __str__(self):
    #     # return json.dumps({'id': str(self.id), 'username': self.username})

    def obj(self):
        return {'id': str(self.id), 'username': self.username}


class UsersView(ViewSet):

    def get(self, request):
        return JsonResponse({'users': [i.obj() for i in registered_users]})

    def delete(self, request):
        print('delete')
        return HttpResponse()

    def post(self, request):
        return self.create_user(request)

    def create_user(self, request):
        body = json.loads(request.body.decode('utf-8'))
        user = body['username']
        is_user_present = len(list(filter(lambda x: x.username == user, registered_users))) == 0
        if is_user_present:
            registered_users.append(User(body['username'], body['password']))
            return JsonResponse({'message': 'Successfully created user'}, status=201)
        else:
            return JsonResponse({'message': 'User with such username already exists'}, status=409)


class SingleUserView(ViewSet):
    def get(self, request, user_id: int):
        for u in registered_users:
            if u.id == int(user_id):
                return JsonResponse({'user': u.obj()})
        return JsonResponse({'message': 'User wasn\'t found'})

    def update(self, request, user_id):
        body = json.loads(request.body.decode('utf-8'))
        user = [x for x in registered_users if x.username == body['username'] and x.id == int(user_id)]
        if len(user) == 0:
            return JsonResponse({'message': 'Unable update user'}, status=409)
        user[0].password_hash = get_hash(body['password'])
        return JsonResponse({'message': 'Successfully updated user'})


class UserLogin(ViewSet):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        user = [x for x in registered_users if x.username == body['username']]
        if len(user) == 0:
            return JsonResponse({'message': 'User wasn\'t found'}, status=401)
        elif user[0].password_hash != get_hash(body['password']):
            return JsonResponse({'message': 'Password is incorrect'}, status=401)
        user_token = create_user_token(user[0])
        return JsonResponse({'access_token': user_token}, status=201)


def create_user_token(user):
    return jwt.encode({'username': user.username, 'exp': (datetime.now() + timedelta(seconds=5)).timestamp()},
                      user.password_hash, algorithm='HS256').decode()


def get_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
