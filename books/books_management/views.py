from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
import json
import jwt

registered_users = {}
user_tokens = {}


def register(request):
    # if request.method == 'POST':
    return register_user(request)
    # return HttpResponse()


def register_user(request):
    body = json.loads(request.body.decode('utf-8'))
    user = body['username']
    if user in registered_users:
        return JsonResponse({'message': 'User with such username already exists'}, status=409)
    else:
        registered_users[user] = body['password']
        return JsonResponse({'message': 'Successfully created user'}, status=201)


def login(request):
    body = json.loads(request.body.decode('utf-8'))
    user = body['username']
    if user not in registered_users:
        return JsonResponse({'message': 'User with such username does not exist'}, status=401)
    elif registered_users[user] != body['password']:
        return JsonResponse({'message': 'Password is incorrect'}, status=401)
    if user in user_tokens:
        user_record = user_tokens[user]
        if user_record['expires_in'] > datetime.now():
            return JsonResponse(user_record, status=201)
        else:
            user_tokens[user] = create_user_token(body)
        return JsonResponse(user_tokens[user], status=201)
    else:
        user_tokens[user] = create_user_token(body)
        return JsonResponse(user_tokens[user], status=201)


def create_user_token(body):
    user_record = {'access_token': jwt.encode(body, body['password'], algorithm='HS256').decode(),
                   # 'expires_in': datetime.now() + timedelta(days=1)}
                   'expires_in': datetime.now() + timedelta(seconds=5)}
    return user_record
