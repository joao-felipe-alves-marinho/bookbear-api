from typing import List

from django.shortcuts import aget_object_or_404
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Book
from BookBearApi.schemas import BookSchema


@api_controller('/book', tags=['book'], permissions=[permissions.AllowAny], auth=None)
class BookController(ControllerBase):
    @route.get('/', response=List[BookSchema])
    async def list_books(self):
        """
        List all books.
        :return: List[BookSchema]
        """
        return [book async for book in Book.objects.all()]

    @route.get('/{book_id}', response=BookSchema)
    async def get_book(self, book_id: int):
        """
        Get a book by id.
        :param book_id: int
        :return: BookSchema
        """
        return await aget_object_or_404(Book, id=book_id)