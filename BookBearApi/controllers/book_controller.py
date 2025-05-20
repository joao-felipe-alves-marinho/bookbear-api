from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja.pagination import paginate
from ninja_extra.ordering import ordering, Ordering
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Book
from BookBearApi.schemas import BookSchema, FilterBookSchema
from BookBearApi.schemas.pagination_schema import AsyncPageNumberPagination


@api_controller('/book', tags=['book'], permissions=[permissions.AllowAny], auth=None)
class BookController(ControllerBase):
    @route.get('/', response=List[BookSchema])
    @paginate(AsyncPageNumberPagination)
    @ordering(Ordering, ordering_fields=['title', 'score'])
    async def get_books(self, filters: FilterBookSchema = Query(...)):
        """
        Get a list of books.
        :return: List[BookSchema]
        """
        return [book async for book in filters.filter(Book.objects.all())]

    @route.get('/{book_id}', response=BookSchema)
    async def get_book(self, book_id: int):
        """
        Get a book by id.
        :param book_id: int
        :return: BookSchema
        """
        return await aget_object_or_404(Book, id=book_id)
