from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ViewSet
from .models import Review


class ReviewsView(ViewSet):

    def get(self, request, book_id):
        all_reviews = Review.objects.filter(book_id=book_id)
        return JsonResponse([r.obj() for r in all_reviews], safe=False)

    def post(self, request, book_id):
        print('post')
        return HttpResponse()


class SingleReviewView(ViewSet):

    def get(self, request, book_id, review_id):
        print('get ', review_id)
        return HttpResponse()

    def update(self, request, book_id, review_id):
        print('update ', review_id)
        return HttpResponse()

    def delete(self, request, book_id, review_id):
        print('delete ', review_id)
        return HttpResponse()
