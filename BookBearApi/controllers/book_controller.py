from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja.pagination import paginate
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)
from ninja_extra.ordering import ordering, Ordering

from BookBearApi.models import Book
from BookBearApi.schemas import BookSchema, FilterBookSchema, AsyncPageNumberPagination, BookRelationshipSchema


@api_controller('/book', tags=['book'], permissions=[permissions.AllowAny], auth=None)
class BookController(ControllerBase):
    @route.get('/', response=List[BookRelationshipSchema])
    @paginate(AsyncPageNumberPagination)
    @ordering(Ordering, ordering_fields=['id', 'title', 'score'])
    async def get_books(self, filters: FilterBookSchema = Query(...)):
        """
        Get a list of books.
        :return: List[BookSchema]
        """
        return [book async for book in filters.filter(Book.objects.all())]

    @route.get('/{int:book_id}', response=BookSchema)
    async def get_book(self, book_id: int):
        """
        Get a book by id.
        :param book_id: int
        :return: BookSchema
        """
        return await aget_object_or_404(Book, id=book_id)
