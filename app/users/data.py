# from .models import User
from app.users.models import User

registered_users = []


class UsersData:

    def add(self, user: User):
        if user not in registered_users:
            registered_users.append(user)
            return True
        return False

    def delete(self, user: User):
        try:
            registered_users.remove(user)
            return user
        except ValueError:
            raise Exception('User not found')

    def update(self, user: User, new_password_hash: str):
        try:
            i = registered_users.index(user)
            registered_users[i].password_hash = new_password_hash
            return True
        except ValueError:
            return False

    def get(self, **params):
        user_id = params.get('id')
        return [x for x in registered_users if user_id is None or x.id == user_id]
