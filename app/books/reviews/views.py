from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ViewSet
from .models import Review


class ReviewsView(ViewSet):

    def get(self, request, book_id):
        all_reviews = Review.objects.filter(book_id=book_id)
        return JsonResponse([r.obj() for r in all_reviews], safe=False)

    def post(self, request, book_id):
        print('post')
        review = request.data.get('review')
        reviewed_by = request.data.get('reviewed_by')
        if review and reviewed_by:
            new_review = Review.objects.create(review=review, book_id_id=book_id, reviewed_by_id=reviewed_by)
            return JsonResponse({'message': 'Successfully created review, id: ' + str(new_review.id)}, status=201)
        return JsonResponse({'message': 'Invalid data'}, status=400)


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
