from django.http import JsonResponse, HttpResponse
from rest_framework.viewsets import ViewSet
from .models import Book
from django.core.exceptions import ObjectDoesNotExist


class BooksView(ViewSet):

    def get(self, request):
        all_books = list(Book.objects.all())
        return JsonResponse({'books': [b.obj() for b in all_books]})

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        if name:
            new_book = Book.objects.create(name=name, description=description)
            return JsonResponse({'message': 'Successfully created book, id: ' + str(new_book.id)}, status=201)
        return JsonResponse({'message': 'Invalid data'}, status=400)


class SingleBookView(ViewSet):

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            return JsonResponse({'book': book.obj()})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)

    def delete(self, request, book_id):
        try:
            removed_book = Book.objects.get(id=book_id)
            result = Book.objects.filter(id=book_id).delete()
            if result[0] == 0:
                return JsonResponse({'message': 'Unable to remove book'}, status=204)
            response_message = {'message': 'removed book'}
            response_message['book'] = removed_book.obj()
            return JsonResponse(response_message)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)

    def update(self, request):
        print('update')
        return HttpResponse()
