from django.conf.urls import url
from django.urls import include
from . import views

urlpatterns = [
    url('^$', views.BooksView.as_view(
        {
            'get': 'get',
            'post': 'post'
        }
    ), name='books_list'),
    url('^(?P<book_id>[0-9]+)/?$', views.SingleBookView.as_view(
        {
            'get': 'get',
            'delete': 'delete',
            'put': 'update'
        }), name='book'),
    url('^(?P<book_id>[0-9]+)/reviews/?', include('app.books.reviews.urls')),
]
