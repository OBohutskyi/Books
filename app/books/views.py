from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from .models import Book
from django.core.exceptions import ObjectDoesNotExist
from app.auth import UserAuthentication
from .permissions import book_write_permission


class BooksView(ViewSet):
    authentication_classes = (UserAuthentication,)

    def get(self, request):
        all_books = list(Book.objects.all())
        return JsonResponse({'books': [b.obj() for b in all_books]})

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        creator_id = request.data.get('creator')
        if name and creator_id:
            new_book = Book.objects.create(name=name, description=description, creator_id=creator_id)
            return JsonResponse({'message': 'Successfully created book, id: ' + str(new_book.id)}, status=201)
        return JsonResponse({'message': 'Invalid data'}, status=400)


class SingleBookView(ViewSet):
    authentication_classes = (UserAuthentication,)

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            return JsonResponse({'book': book.obj()})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)

    @book_write_permission
    def delete(self, request, book_id):
        try:
            removed_book = Book.objects.get(id=book_id)
            Book.objects.filter(id=book_id).delete()
            response_message = {'message': 'removed book'}
            response_message['book'] = removed_book.obj()
            return JsonResponse(response_message)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)

    @book_write_permission
    def update(self, request, book_id):
        name = request.data.get('name')
        description = request.data.get('description')
        if name or description:
            try:
                existing_book = Book.objects.filter(id=book_id)
                if not existing_book:
                    return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)
                if name:
                    existing_book.update(name=name)
                if description:
                    existing_book.update(description=description)
                return JsonResponse({'message': 'Successfully updated book', 'book': existing_book[0].obj()})
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'Book doesn\'t exist'}, status=401)
        return JsonResponse({'message': 'Invalid data'}, status=400)
