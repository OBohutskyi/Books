from app.users.models import User

registered_users = []


class UsersData:

    def add(self, user: User):
        if user.username not in list(map(lambda x: x.username, registered_users)):
            registered_users.append(user)
            return True
        return False

    def delete(self, user_id: str):
        temp = [x for x in registered_users if str(x.id) == user_id]
        if temp:
            registered_users.remove(temp[0])
            return temp[0]
        else:
            raise Exception('User not found')

    def update(self, user_id: str, new_password_hash: str):
        temp = [x for x in registered_users if str(x.id) == user_id]
        if temp:
            temp[0].password_hash = new_password_hash
            return True
        else:
            return False

    def get(self, **params):
        user_id = params.get('id')
        return [x for x in registered_users if user_id is None or str(x.id) == user_id]

    def is_user_present(self, username: str):
        temp = [x for x in registered_users if x.username == username]
        if temp:
            return temp[0]
        else:
            return False
