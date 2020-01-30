from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.ReviewsView.as_view(
        {
            'get': 'get',
            'post': 'post'
        }
    ), name='reviews_list'),
    url('^(?P<review_id>[0-9]+)/?$', views.SingleReviewView.as_view(
        {
            'get': 'get',
            'delete': 'delete',
            'put': 'update'
        }), name='review'),
]