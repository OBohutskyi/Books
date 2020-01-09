from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.UsersView.as_view(
        {
            'get': 'get',
            'delete': 'delete',
            'post': 'post'
        }
    ), name='users_list'),
    url('^(?P<user_id>[0-9]+)/?$', views.SingleUserView.as_view(
        {
            'get': 'get',
            'put': 'update'
        }), name='user'),
    url('me/', views.UserLogin.as_view(
        {
            'post': 'post'
        }), name='login')
]
