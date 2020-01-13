from django.test import Client
from django.urls import reverse


class TestUsersView:

    def test_get_returns_all_users(self):
        resp = Client().get(reverse('users_list'))
        assert {'users': []} == resp.json()
